#!/usr/bin/env python3
"""findings_store.py — Dedup store for 7B audit findings.
SQLite + SHA256 fingerprints + nomic-embed-text semantic matching.
Duplicate = exact fingerprint match OR cosine sim >= 0.92 vs same file.
Stdlib only. Idempotent. Absolute paths. Self-test: --selftest"""

import hashlib
import json
import re
import sqlite3
import struct
import sys
import urllib.request
import zlib
from pathlib import Path

DB_PATH = Path("/home/jesse/src/openroot-thesis/audit_reports/findings.db")
EMBED_URL = "http://127.0.0.1:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
SIM_THRESHOLD = 0.92

SCHEMA = """
CREATE TABLE IF NOT EXISTS findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fingerprint TEXT NOT NULL UNIQUE,
    file TEXT NOT NULL,
    line INTEGER,
    severity TEXT NOT NULL,
    issue TEXT NOT NULL,
    fix TEXT NOT NULL,
    embedding BLOB,
    first_seen TEXT DEFAULT (datetime('now')),
    last_seen TEXT DEFAULT (datetime('now')),
    times_seen INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_findings_file ON findings(file);
"""

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH, timeout=30)
    db.executescript(SCHEMA)
    return db

def normalize_issue(text: str) -> str:
    words = re.findall(r"[a-z0-9_]+", (text or "").lower())
    return " ".join(w for w in words if len(w) > 1)

def fingerprint(fname: str, line, issue: str) -> str:
    raw = f"{Path(fname).name}|{line}|{normalize_issue(issue)}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def embed(text: str):
    """768-dim nomic embedding packed+compressed, or None if unavailable."""
    try:
        payload = json.dumps({"model": EMBED_MODEL, "prompt": text or ""}).encode()
        req = urllib.request.Request(EMBED_URL, data=payload,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            vec = json.loads(r.read())["embedding"]
        blob = zlib.compress(struct.pack(f"<{len(vec)}f", *vec))
        return sqlite3.Binary(blob)
    except Exception:
        return None

def decompress(blob):
    if not blob:
        return None
    raw = zlib.decompress(bytes(blob))
    n = len(raw) // 4
    return list(struct.unpack(f"<{n}f", raw))

def cosine(a, b):
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5 or 1.0
    nb = sum(x * x for x in b) ** 0.5 or 1.0
    return dot / (na * nb)

def add(findings: list):
    """Insert/dedupe findings. Returns (new_count, dup_count, embeds_ok)."""
    db = connect()
    new_rows, dup = [], 0
    embeds_ok = 0
    for f in findings:
        fname = f.get("file", "")
        line = f.get("line")
        issue = f.get("issue", "") or ""
        fp = fingerprint(fname, line, issue)
        row = db.execute("SELECT id FROM findings WHERE fingerprint=?", (fp,)).fetchone()
        if row:
            db.execute("""UPDATE findings SET times_seen=times_seen+1,
                          last_seen=datetime('now') WHERE id=?""", (row[0],))
            dup += 1
            continue
        vec_blob = embed(issue)
        if vec_blob is not None:
            vec = decompress(vec_blob)
            sem_dup = False
            for (blob,) in db.execute(
                    "SELECT embedding FROM findings WHERE file=? AND embedding IS NOT NULL",
                    (fname,)):
                if cosine(vec, decompress(blob)) >= SIM_THRESHOLD:
                    db.execute("""UPDATE findings SET times_seen=times_seen+1,
                                  last_seen=datetime('now') WHERE file=?""",
                               (fname,))
                    dup += 1
                    sem_dup = True
                    break
            if sem_dup:
                continue
            embeds_ok += 1
        new_rows.append((fp, fname, line, f.get("severity", "info"),
                         issue, f.get("fix", ""), vec_blob))
    db.executemany("""INSERT INTO findings
        (fingerprint,file,line,severity,issue,fix,embedding)
        VALUES (?,?,?,?,?,?,?)""", new_rows)
    db.commit()
    db.close()
    return len(new_rows), dup, embeds_ok

def report():
    db = connect()
    rows = db.execute("""SELECT severity, file, COUNT(*), MAX(times_seen)
                         FROM findings GROUP BY severity, file ORDER BY severity""").fetchall()
    for sev, f, n, seen in rows:
        print(f"  {sev:<8} {f:<50} {n:>3} findings (max seen x{seen})")
    total, = db.execute("SELECT COUNT(*) FROM findings").fetchone()
    print(f"  total unique findings: {total}")
    db.close()

def selftest():
    """Two same-issue findings: exact dup then paraphrase (if embeddings live)."""
    base = [{"file": "code/python/selftest.py", "line": 10,
             "severity": "critical", "issue": "silent except pass swallows errors",
             "fix": "log and re-raise"}]
    n1, d1, e1 = add(base)
    again = [dict(base[0])]  # identical -> fingerprint dup
    para = [dict(base[0], line=20,
                 issue="exception handling missing around file write, errors hidden")]
    n2, d2, e2 = add(again + para)
    print(f"pass1: new={n1} dup={d1} embeds={e1} (expect new=1 dup=0)")
    print(f"pass2: new={n2} dup={d2} embeds={e2} (expect dup>=1; paraphrase caught if embeddings live)")
    report()

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    elif "--report" in sys.argv:
        report()
    else:
        print("Usage: findings_store.py --selftest | --report | import as module")
