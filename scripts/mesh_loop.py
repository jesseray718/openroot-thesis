#!/usr/bin/env python3
"""
mesh_loop.py — bounded local-first maintenance loop for OpenRoot.

Modes:
  collect       Import mesh state and audit JSON reports into SQLite.
  queue         Create deduplicated, ranked tasks from collected evidence.
  status        Show the next actionable tasks.
  propose ID    Retrieve bounded evidence and ask local Ollama 7B for JSON.
  show ID       Print the stored proposal.
  branch ID     Create a local git branch and proposal file; never pushes.
  verify ID     Run limited local verification for the proposal branch.

Safety:
  - No automatic commit, push, PR, issue modification, deletion, or credentials.
  - The model receives bounded evidence and returns a proposal only.
  - SQLite is the durable source of truth; model output is untrusted.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path("/home/jesse/src/openroot-thesis").resolve()
REPORTS = ROOT / "audit_reports"
DB_PATH = REPORTS / "mesh_memory.db"
PROPOSALS = ROOT / "generated_proposals"

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:7b")

MAX_EVIDENCE_CHARS = 14000
MAX_SOURCE_CHARS = 9000
MAX_PATCH_LINES = 220
MIN_CONFIDENCE = 0.60

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,
    started_at TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at TEXT,
    status TEXT NOT NULL DEFAULT 'running',
    detail TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY,
    source_path TEXT NOT NULL,
    source_kind TEXT NOT NULL,
    content_hash TEXT NOT NULL UNIQUE,
    collected_at TEXT NOT NULL DEFAULT (datetime('now')),
    text TEXT NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS evidence_fts USING fts5(
    text, source_path UNINDEXED, source_kind UNINDEXED
);

CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    fingerprint TEXT NOT NULL UNIQUE,
    repo TEXT NOT NULL,
    branch TEXT NOT NULL DEFAULT 'main',
    kind TEXT NOT NULL,
    title TEXT NOT NULL,
    detail TEXT NOT NULL,
    severity INTEGER NOT NULL DEFAULT 1,
    reach INTEGER NOT NULL DEFAULT 1,
    durability REAL NOT NULL DEFAULT 1.0,
    reuse REAL NOT NULL DEFAULT 1.0,
    time_cost REAL NOT NULL DEFAULT 1.0,
    compute_cost REAL NOT NULL DEFAULT 1.0,
    cognitive_cost REAL NOT NULL DEFAULT 1.0,
    risk REAL NOT NULL DEFAULT 1.0,
    evidence_confidence REAL NOT NULL DEFAULT 0.5,
    score REAL NOT NULL DEFAULT 0.0,
    state TEXT NOT NULL DEFAULT 'queued',
    human_approved INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS proposals (
    id INTEGER PRIMARY KEY,
    task_id TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt_hash TEXT NOT NULL,
    raw_response TEXT NOT NULL,
    parsed_json TEXT,
    valid INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY(task_id) REFERENCES tasks(id)
);

CREATE TABLE IF NOT EXISTS outcomes (
    id INTEGER PRIMARY KEY,
    task_id TEXT NOT NULL,
    outcome TEXT NOT NULL,
    detail TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY(task_id) REFERENCES tasks(id)
);

CREATE INDEX IF NOT EXISTS idx_tasks_state_score ON tasks(state, score DESC);
CREATE INDEX IF NOT EXISTS idx_proposals_task ON proposals(task_id, id DESC);
"""

def now_id():
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")

def db():
    REPORTS.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con

def hash_text(text):
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()

def start_run(con, kind):
    cur = con.execute("INSERT INTO runs(kind) VALUES (?)", (kind,))
    con.commit()
    return cur.lastrowid

def finish_run(con, run_id, status, detail=""):
    con.execute(
        "UPDATE runs SET finished_at=datetime('now'), status=?, detail=? WHERE id=?",
        (status, detail, run_id),
    )
    con.commit()

def git(args, cwd=ROOT, check=True):
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=check,
    )

def repo_for_path(path_text):
    p = Path(path_text)
    try:
        rel = p.resolve().relative_to(ROOT)
    except Exception:
        return "openroot-thesis"
    parts = rel.parts
    return parts[0] if len(parts) > 1 else "openroot-thesis"

def default_branch(repo):
    if repo == "openroot-thesis":
        return "main"
    return "main"

def task_score(severity, reach, durability, reuse, time_cost, compute_cost,
               cognitive_cost, risk, confidence):
    benefit = max(1.0, float(severity)) * max(1.0, float(reach))
    numerator = benefit * max(0.2, durability) * max(0.2, reuse) * max(0.2, confidence)
    denominator = max(1.0, time_cost) * max(1.0, compute_cost) * max(1.0, cognitive_cost) * max(1.0, risk)
    return round(100.0 * numerator / denominator, 2)

def add_evidence(con, source_path, source_kind, text):
    text = text.strip()
    if not text:
        return False
    h = hash_text(source_path + "\n" + text)
    row = con.execute("SELECT id FROM evidence WHERE content_hash=?", (h,)).fetchone()
    if row:
        return False
    con.execute(
        "INSERT INTO evidence(source_path,source_kind,content_hash,text) VALUES (?,?,?,?)",
        (source_path, source_kind, h, text),
    )
    con.execute(
        "INSERT INTO evidence_fts(text,source_path,source_kind) VALUES (?,?,?)",
        (text, source_path, source_kind),
    )
    return True

def make_task(con, repo, branch, kind, title, detail, severity=1, reach=1,
              durability=1.0, reuse=1.0, time_cost=1.0, compute_cost=1.0,
              cognitive_cost=1.0, risk=1.0, confidence=0.5):
    canonical = "|".join([repo, branch, kind, title.strip().lower(), detail.strip().lower()])
    fp = hash_text(canonical)[:24]
    score = task_score(severity, reach, durability, reuse, time_cost, compute_cost,
                       cognitive_cost, risk, confidence)
    task_id = "task-" + fp[:12]
    existing = con.execute("SELECT id FROM tasks WHERE fingerprint=?", (fp,)).fetchone()
    if existing:
        con.execute(
            "UPDATE tasks SET score=?, updated_at=datetime('now') WHERE id=?",
            (score, existing["id"]),
        )
        return False
    con.execute(
        """INSERT INTO tasks(
            id,fingerprint,repo,branch,kind,title,detail,severity,reach,durability,reuse,
            time_cost,compute_cost,cognitive_cost,risk,evidence_confidence,score
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (task_id, fp, repo, branch, kind, title, detail, severity, reach, durability,
         reuse, time_cost, compute_cost, cognitive_cost, risk, confidence, score),
    )
    return True

def collect_json(con, path):
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
        data = json.loads(raw)
    except Exception as exc:
        print(f"SKIP {path.name}: {exc}")
        return 0
    n = 0
    if add_evidence(con, str(path), "json-report", raw[:50000]):
        n += 1
    if path.name == "mesh_state.json" and isinstance(data, list):
        for item in data:
            repo = item.get("repo", "openroot-thesis")
            detail = (
                f"Repository health: deficit={item.get('deficit')}, "
                f"open_items={item.get('open_items')}, age_days={item.get('age_days')}, "
                f"has_ci={item.get('has_ci')}."
            )
            issues = int(item.get("open_items") or 0)
            if issues > 0:
                make_task(
                    con, repo, default_branch(repo), "triage",
                    f"Triage {issues} open issue(s) in {repo}",
                    detail, severity=2, reach=min(4, max(1, issues)),
                    durability=1.4, reuse=1.2, time_cost=1.0,
                    compute_cost=1.0, cognitive_cost=1.0, risk=1.0, confidence=0.85,
                )
    if isinstance(data, dict):
        files = data.get("files", {})
        if isinstance(files, dict):
            for fname, result in files.items():
                for finding in result.get("findings", []) or []:
                    issue = str(finding.get("issue", "")).strip()
                    if not issue:
                        continue
                    sev_name = str(finding.get("severity", "info")).lower()
                    sev = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 1}.get(sev_name, 1)
                    fix = str(finding.get("fix", "")).strip()
                    line = finding.get("line", "?")
                    detail = f"File: {fname}; line: {line}; issue: {issue}; suggested fix: {fix}"
                    make_task(
                        con, "openroot-thesis", "main", "audit-fix",
                        f"{sev_name}: {issue[:120]}",
                        detail, severity=sev, reach=2 if sev >= 3 else 1,
                        durability=1.5, reuse=1.25, time_cost=1.0,
                        compute_cost=1.0, cognitive_cost=1.0,
                        risk=1.2 if sev >= 3 else 1.0, confidence=0.75,
                    )
    return n

def cmd_collect(args):
    con = db()
    run_id = start_run(con, "collect")
    total = 0
    for path in sorted(REPORTS.glob("*.json")):
        total += collect_json(con, path)
    con.commit()
    finish_run(con, run_id, "ok", f"new_evidence={total}")
    print(f"COLLECT OK: {total} new evidence record(s)")
    print(f"DB: {DB_PATH}")

def cmd_queue(args):
    con = db()
    run_id = start_run(con, "queue")
    rows = con.execute(
        """SELECT id, repo, title, detail, severity, reach, durability, reuse,
                  time_cost, compute_cost, cognitive_cost, risk, evidence_confidence
           FROM tasks WHERE state IN ('queued','proposed')"""
    ).fetchall()
    for r in rows:
        score = task_score(
            r["severity"], r["reach"], r["durability"], r["reuse"],
            r["time_cost"], r["compute_cost"], r["cognitive_cost"],
            r["risk"], r["evidence_confidence"],
        )
        con.execute("UPDATE tasks SET score=?, updated_at=datetime('now') WHERE id=?",
                    (score, r["id"]))
    con.commit()
    finish_run(con, run_id, "ok", f"rescored={len(rows)}")
    print(f"QUEUE OK: rescored {len(rows)} task(s)")
    if not hasattr(args, "limit"):
        args.limit = 12
    cmd_status(args)

def cmd_status(args):
    con = db()
    rows = con.execute(
        """SELECT id, repo, branch, kind, score, state, title
           FROM tasks
           WHERE state IN ('queued','proposed','reviewed','branched')
           ORDER BY score DESC, created_at ASC
           LIMIT ?""",
        (args.limit,),
    ).fetchall()
    if not rows:
        print("No active tasks. Run: python3 scripts/mesh_loop.py collect")
        return
    print(f"{'ID':<19} {'SCORE':>7} {'STATE':<9} {'REPO':<24} TITLE")
    print("-" * 110)
    for r in rows:
        print(f"{r['id']:<19} {r['score']:>7.2f} {r['state']:<9} {r['repo']:<24} {r['title']}")

def find_task(con, task_id):
    row = con.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if not row:
        raise SystemExit(f"Task not found: {task_id}. Run status to list tasks.")
    return row

def source_evidence(task):
    chunks = [f"TASK\nid: {task['id']}\nrepo: {task['repo']}\nbranch: {task['branch']}\n"
              f"kind: {task['kind']}\ntitle: {task['title']}\ndetail: {task['detail']}\n"
              f"score: {task['score']}"]
    text = task["detail"]
    paths = re.findall(r"(?:File:\s*)?([A-Za-z0-9_./-]+\.py)", text)
    for rel in paths[:2]:
        p = Path(rel)
        if not p.is_absolute():
            p = ROOT / p
        try:
            if p.is_file() and p.resolve().is_relative_to(ROOT):
                body = p.read_text(encoding="utf-8", errors="replace")[:MAX_SOURCE_CHARS]
                chunks.append(f"\nSOURCE {p.relative_to(ROOT)}\n{body}")
        except Exception:
            pass
    return "\n".join(chunks)[:MAX_EVIDENCE_CHARS]

def model_prompt(task, evidence):
    return f"""You are a constrained local software-maintenance planner.

Return exactly one valid JSON object. No Markdown fences. No prose before or after JSON.
You are not authorized to execute commands, change files, commit, push, create issues,
access credentials, or propose changes outside the allowed repository.

Allowed repository: {task['repo']}
Allowed branch: {task['branch']}
Task: {task['title']}
Task detail: {task['detail']}

Rules:
- Prefer the smallest safe change.
- If evidence is insufficient, return decision="needs_more_evidence".
- Do not invent paths, tests, APIs, or facts.
- Proposed patch must be a unified diff and no more than {MAX_PATCH_LINES} lines.
- Do not modify workflow files, .git files, secrets, dependencies, or CI configuration.
- Only propose a patch if a source path is present in the evidence.
- Include objective local tests; Python syntax compilation is acceptable when no test exists.

Required JSON schema:
{{
  "decision": "propose_patch|needs_more_evidence|no_change",
  "confidence": 0.0,
  "summary": "short factual summary",
  "evidence_used": ["short references to supplied evidence only"],
  "files_to_change": ["relative/path"],
  "plan": ["step"],
  "patch_unified_diff": "diff text or empty string",
  "tests": ["command"],
  "risks": ["risk"],
  "rollback": "how to revert"
}}

EVIDENCE START
{evidence}
EVIDENCE END
"""

def call_ollama(prompt):
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 1800},
    }).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=240) as response:
        data = json.loads(response.read().decode("utf-8", "replace"))
    return str(data.get("response", "")).strip()

def validate_proposal(task, raw):
    reasons = []
    parsed = None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        return False, None, [f"invalid JSON: {exc}"]

    required = {
        "decision", "confidence", "summary", "evidence_used", "files_to_change",
        "plan", "patch_unified_diff", "tests", "risks", "rollback",
    }
    missing = sorted(required - set(parsed))
    if missing:
        reasons.append("missing keys: " + ", ".join(missing))

    if parsed.get("decision") not in {"propose_patch", "needs_more_evidence", "no_change"}:
        reasons.append("invalid decision")

    try:
        confidence = float(parsed.get("confidence", 0))
        if not 0 <= confidence <= 1:
            reasons.append("confidence must be 0..1")
    except Exception:
        reasons.append("confidence is not numeric")
        confidence = 0

    files = parsed.get("files_to_change", [])
    if not isinstance(files, list):
        reasons.append("files_to_change must be a list")
        files = []

    forbidden = (".github/", ".git/", "../", "/etc/", "/home/", "requirements", "pyproject.toml")
    for f in files:
        if not isinstance(f, str) or not f or f.startswith("/") or any(x in f for x in forbidden):
            reasons.append(f"forbidden path: {f!r}")
        elif not (ROOT / f).exists():
            reasons.append(f"path does not exist: {f}")

    diff = str(parsed.get("patch_unified_diff", ""))
    if parsed.get("decision") == "propose_patch":
        if confidence < MIN_CONFIDENCE:
            reasons.append(f"confidence below {MIN_CONFIDENCE}")
        if not diff.startswith("--- "):
            reasons.append("patch must begin with a unified diff header")
        if len(diff.splitlines()) > MAX_PATCH_LINES:
            reasons.append("patch exceeds maximum line count")
        for marker in ("rm -rf", "curl ", "wget ", "sudo ", "chmod 777", "subprocess", "os.system"):
            if marker in diff.lower():
                reasons.append(f"forbidden patch content: {marker}")
    return not reasons, parsed, reasons

def cmd_propose(args):
    con = db()
    task = find_task(con, args.task_id)
    if task["state"] in {"applied", "closed"}:
        raise SystemExit("Task is already closed; create a new task if new evidence exists.")
    evidence = source_evidence(task)
    prompt = model_prompt(task, evidence)
    prompt_hash = hash_text(prompt)
    print(f"Calling local model: {OLLAMA_MODEL}")
    try:
        raw = call_ollama(prompt)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Ollama call failed: {exc}\nCheck: ollama list ; curl http://127.0.0.1:11434/api/tags")
    valid, parsed, reasons = validate_proposal(task, raw)
    con.execute(
        """INSERT INTO proposals(task_id,model,prompt_hash,raw_response,parsed_json,valid)
           VALUES (?,?,?,?,?,?)""",
        (task["id"], OLLAMA_MODEL, prompt_hash, raw,
         json.dumps(parsed, indent=2) if parsed else None, int(valid)),
    )
    con.execute(
        "UPDATE tasks SET state=?, updated_at=datetime('now') WHERE id=?",
        ("proposed" if valid else "queued", task["id"]),
    )
    con.commit()
    print(f"PROPOSAL {'VALID' if valid else 'REJECTED'} for {task['id']}")
    if reasons:
        print("Reasons:")
        for reason in reasons:
            print(" -", reason)
    proposal_path = PROPOSALS / f"{task['id']}-latest.json"
    proposal_path.write_text(json.dumps(parsed, indent=2) if parsed else raw + "\n",
                             encoding="utf-8")
    print(f"Saved: {proposal_path}")

def latest_proposal(con, task_id):
    row = con.execute(
        """SELECT * FROM proposals WHERE task_id=? ORDER BY id DESC LIMIT 1""",
        (task_id,),
    ).fetchone()
    if not row:
        raise SystemExit("No proposal exists. Run propose TASK_ID first.")
    return row

def cmd_show(args):
    con = db()
    task = find_task(con, args.task_id)
    prop = latest_proposal(con, task["id"])
    print(prop["parsed_json"] or prop["raw_response"])
    print(f"\nvalid={bool(prop['valid'])}; model={prop['model']}; created={prop['created_at']}")

def cmd_branch(args):
    con = db()
    task = find_task(con, args.task_id)
    prop = latest_proposal(con, task["id"])
    if not prop["valid"]:
        raise SystemExit("Latest proposal is not valid; no branch will be created.")
    data = json.loads(prop["parsed_json"])
    if data["decision"] != "propose_patch":
        raise SystemExit(f"Proposal decision is {data['decision']}; no patch branch needed.")

    branch = f"mesh/{task['id']}"
    existing = git(["branch", "--list", branch], check=False).stdout.strip()
    if existing:
        raise SystemExit(f"Branch already exists: {branch}. Inspect it manually.")
    status = git(["status", "--porcelain"]).stdout.strip()
    if status:
        raise SystemExit("Working tree is not clean. Commit/stash/review changes before branching.")

    git(["switch", "-c", branch])
    patch = data["patch_unified_diff"]
    patch_path = PROPOSALS / f"{task['id']}.patch"
    patch_path.write_text(patch + "\n", encoding="utf-8")
    applied = subprocess.run(["git", "apply", "--check", str(patch_path)],
                             cwd=ROOT, text=True, capture_output=True)
    if applied.returncode != 0:
        git(["switch", task["branch"]], check=False)
        raise SystemExit("Patch failed git-apply check; branch retained for inspection:\n" + applied.stderr)
    applied = subprocess.run(["git", "apply", str(patch_path)],
                             cwd=ROOT, text=True, capture_output=True)
    if applied.returncode != 0:
        raise SystemExit("Patch application failed:\n" + applied.stderr)

    con.execute("UPDATE tasks SET state='branched', updated_at=datetime('now') WHERE id=?",
                (task["id"],))
    con.execute("INSERT INTO outcomes(task_id,outcome,detail) VALUES (?,?,?)",
                (task["id"], "branch-created", branch))
    con.commit()
    print(f"PATCH APPLIED LOCALLY on branch: {branch}")
    print("Nothing was committed or pushed.")
    print("Next: python3 scripts/mesh_loop.py verify " + task["id"])
    print("Then inspect: git diff")

def cmd_verify(args):
    con = db()
    task = find_task(con, args.task_id)
    prop = latest_proposal(con, task["id"])
    if not prop["valid"]:
        raise SystemExit("Latest proposal invalid.")
    data = json.loads(prop["parsed_json"])
    tests = data.get("tests", [])
    if not tests:
        raise SystemExit("No tests listed; refuse to run.")
    allowed_prefixes = ("python3 -m py_compile ", "python3 -m unittest ", "pytest ")
    results = []
    for command in tests:
        if not isinstance(command, str) or not command.startswith(allowed_prefixes):
            results.append((command, 126, "REFUSED: command outside test allowlist"))
            continue
        run = subprocess.run(command, cwd=ROOT, shell=True, text=True,
                             capture_output=True, timeout=120)
        output = (run.stdout + run.stderr)[-3000:]
        results.append((command, run.returncode, output))
    ok = all(code == 0 for _, code, _ in results)
    detail = "\n\n".join(f"$ {cmd}\nexit={code}\n{out}" for cmd, code, out in results)
    con.execute("INSERT INTO outcomes(task_id,outcome,detail) VALUES (?,?,?)",
                (task["id"], "verify-pass" if ok else "verify-fail", detail))
    con.execute("UPDATE tasks SET state=?, updated_at=datetime('now') WHERE id=?",
                ("reviewed" if ok else "branched", task["id"]))
    con.commit()
    print("VERIFY", "PASS" if ok else "FAIL")
    for command, code, _ in results:
        print(f"exit={code}  {command}")
    log = PROPOSALS / f"{task['id']}-verify.log"
    log.write_text(detail + "\n", encoding="utf-8")
    print(f"Saved: {log}")
    if ok:
        print("Review with: git diff")
        print("If you approve manually: git add <files> && git commit -m 'fix: ...' && git push -u origin HEAD")
    else:
        print("Do not commit. Inspect the log and revert if needed: git restore .")

def main():
    parser = argparse.ArgumentParser(description="Bounded local 7B maintenance loop")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("collect")
    sub.add_parser("queue")
    p_status = sub.add_parser("status")
    p_status.add_argument("--limit", type=int, default=12)
    p_prop = sub.add_parser("propose")
    p_prop.add_argument("task_id")
    p_show = sub.add_parser("show")
    p_show.add_argument("task_id")
    p_branch = sub.add_parser("branch")
    p_branch.add_argument("task_id")
    p_verify = sub.add_parser("verify")
    p_verify.add_argument("task_id")
    args = parser.parse_args()
    {
        "collect": cmd_collect,
        "queue": cmd_queue,
        "status": cmd_status,
        "propose": cmd_propose,
        "show": cmd_show,
        "branch": cmd_branch,
        "verify": cmd_verify,
    }[args.cmd](args)

if __name__ == "__main__":
    main()
