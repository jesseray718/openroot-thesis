#!/usr/bin/env python3
"""ai_audit.py — 7B-model GitHub optimization audit (AGAPE_NET node).
Setup mode: installs ollama + model, verifies gh, writes workflow.
Agent mode (--agent): audits files changed in latest commit via local 7B,
writes structured findings, opens GitHub issue on critical severity.
Stdlib only. Idempotent. Absolute paths. Fails loud."""

import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO = Path("/home/jesse/src/openroot-thesis")
REPORTS = REPO / "audit_reports"
WORKFLOW = REPO / ".github/workflows/audit.yml"
MODEL = "qwen2.5-coder:7b"           # best 7B coder; 4.7GB q4_K_M quant
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MAX_FILE_BYTES = 60_000                # keep context small enough for 7B
MAX_ISSUE_SEVERITY_GATE = "critical"

SYSTEM_PROMPT = (
    "You are a strict code auditor. You receive ONE file. Return ONLY a JSON "
    "object, no markdown, no prose outside JSON. Schema: "
    '{"findings":[{"line":<int>,"severity":"info|minor|major|critical",'
    '"issue":"<one sentence>","fix":"<one sentence actionable fix>"}],'
    '"effort_score":<1-10>, "quality_score":<1-10>} '
    "Judge: correctness bugs, resource waste, non-idempotent operations, "
    "silent failure paths, hardcoded relative paths, missing error handling. "
    "Quality bar: maximum output per unit of effort. If the file is clean, "
    "return an empty findings array. Never invent issues to seem useful."
)

def run(cmd, cwd=None, check=False):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)

def sh(c, cwd=None):
    return subprocess.run(c, cwd=cwd, shell=True, capture_output=True, text=True)

def ollama_ready():
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=3) as r:
            return True
    except Exception:
        return False

def setup():
    # 1. Ollama binary
    if not shutil.which("ollama") and not Path("/usr/local/bin/ollama").is_file():
        r = sh('curl -fsSL https://ollama.com/install.sh | sh')
        if r.returncode != 0:
            sys.exit("ERROR: ollama install failed (needs sudo or network):\n" + r.stderr)
    if not ollama_ready():
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import time
        for _ in range(20):
            if ollama_ready():
                break
            time.sleep(0.5)
    if not ollama_ready():
        sys.exit("ERROR: ollama daemon not reachable at 127.0.0.1:11434")

    # 2. Model (idempotent pull)
    have = {m.get("name") for m in json.load(
        urllib.request.urlopen("http://127.0.0.1:11434/api/tags")).get("models", [])}
    if MODEL not in have and f"{MODEL}:latest" not in have:
        print(f"Pulling {MODEL} (~4.7GB, one time)...")
        r = subprocess.run(["ollama", "pull", MODEL])
        if r.returncode != 0:
            sys.exit(f"ERROR: model pull failed — check disk/RAM (need ~5GB free)")

    # 3. gh auth
    if not shutil.which("gh"):
        sys.exit("ERROR: install GitHub CLI first: sudo apt-get install -y gh && gh auth login")
    r = run(["gh", "auth", "status"])
    if r.returncode != 0:
        sys.exit("ERROR: gh not authenticated. Run: gh auth login")

    # 4. Workflow (self-hosted runner on this box)
    WORKFLOW.parent.mkdir(parents=True, exist_ok=True)
    WORKFLOW.write_text("""name: ai-audit
on:
  push:
    paths: ["code/**", "scripts/**"]
  workflow_dispatch:
jobs:
  audit:
    runs-on: [self-hosted, optiplex]
    steps:
      - uses: actions/checkout@v4
        with: {fetch-depth: 2}
      - run: python3 /home/jesse/src/openroot-thesis/scripts/ai_audit.py --agent
""")
    print(f"Wrote workflow -> {WORKFLOW}")
    print("\nSETUP COMPLETE. Remaining manual step (one time, ~2 min):")
    print("  1. GitHub repo -> Settings -> Actions -> Runners -> New self-hosted runner")
    print("  2. Run the download/config commands it shows, on this box, as user jesse")
    print("  3. Start it:  /home/jesse/actions-runner/run.sh  (leave terminal open")
    print("     or: ./svc.sh install && ./svc.sh start  for a system service)")
    print("  4. git add .github/workflows/audit.yml scripts/ai_audit.py && commit && push")
    print("\nSmoke test locally first:")
    print("  python3 /home/jesse/src/openroot-thesis/scripts/ai_audit.py --agent --file code/python/uplift_weak_nodes.py")

def changed_files():
    sha = run(["git", "rev-parse", "HEAD"], cwd=REPO).stdout.strip()
    files = run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=REPO).stdout.split()
    return sha, [f for f in files if f.endswith(".py") and (REPO / f).is_file()]

def query_model(source, fname):
    payload = json.dumps({
        "model": MODEL,
        "stream": False,
        "options": {"temperature": 0, "num_ctx": 8192},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"File: {fname}\n```\n{source}\n```"},
        ],
    }).encode()
    req = urllib.request.Request(OLLAMA_URL, data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())["message"]["content"]

def parse_findings(raw):
    m = re.search(r"\{.*\}", raw, re.DOTALL)  # tolerate stray prose around JSON
    if not m:
        raise ValueError("no JSON object in model output")
    obj = json.loads(m.group(0))
    assert isinstance(obj.get("findings"), list)
    return obj

def audit_file(fname):
    path = REPO / fname
    source = path.read_text(errors="replace")[:MAX_FILE_BYTES]
    for attempt in range(3):  # validate-retry: the 7B reliability mechanism
        try:
            return parse_findings(query_model(source, fname))
        except (ValueError, json.JSONDecodeError, KeyError, AssertionError) as e:
            print(f"  retry {attempt+1}/3 ({e})")
    return {"findings": [], "parse_failed": True}

def agent(single_file=None):
    if not ollama_ready():
        sys.exit("ERROR: ollama not running (run: ollama serve, or setup mode)")
    REPORTS.mkdir(exist_ok=True)
    if single_file:
        sha = "local-manual"
        files = [single_file]
    else:
        sha, files = changed_files()
        if not files:
            print("No changed .py files to audit.")
            return
    print(f"Auditing {len(files)} file(s) @ {sha[:8]} with {MODEL}")
    report, worst = {"sha": sha, "files": {}}, "info"
    rank = {"info": 0, "minor": 1, "major": 2, "critical": 3}
    for f in files:
        print(f"  -> {f}")
        res = audit_file(f)
        report["files"][f] = res
        for fd in res.get("findings", []):
            sev = fd.get("severity", "info")
            if rank.get(sev, 0) > rank.get(worst, 0):
                worst = sev
    out = REPORTS / f"audit_{sha[:12]}.json"
    out.write_text(json.dumps(report, indent=2))
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import findings_store
        all_f = []
        for _f, _res in report["files"].items():
            for _fd in _res.get("findings", []):
                all_f.append({**_fd, "file": _f})
        if all_f:
            _n, _d, _e = findings_store.add(all_f)
            print(f"Findings store: {_n} new, {_d} duplicates ({_e} embedded)")
    except Exception as _exc:
        print(f"findings_store unavailable (non-fatal): {_exc}")
    print(f"Report -> {out}  (worst severity: {worst})")

    if rank.get(worst, 0) >= rank[MAX_ISSUE_SEVERITY_GATE]:
        body_lines = [f"Automated 7B audit found **{worst}** severity issues.",
                      "", f"Full report: `audit_reports/audit_{sha[:12]}.json`", ""]
        for f, res in report["files"].items():
            for fd in res.get("findings", []):
                if rank.get(fd.get("severity", "info"), 0) >= 2:
                    body_lines.append(
                        f"- `{f}:{fd.get('line','?')}` [{fd.get('severity')}] "
                        f"{fd.get('issue')} — **Fix:** {fd.get('fix')}")
        r = run(["gh", "issue", "create",
                 "--repo", "jesseray718/openroot-thesis",
                 "--title", f"[ai-audit] {worst} findings @ {sha[:8]}",
                 "--body", "\n".join(body_lines)], cwd=REPO)
        print(f"GitHub issue: {r.stdout.strip() or r.stderr.strip()}")

if __name__ == "__main__":
    os.makedirs(REPO / "scripts", exist_ok=True)
    target = str(Path(__file__).resolve())
    dest = REPO / "scripts/ai_audit.py"
    if Path(target) != dest:
        dest.write_text(Path(target).read_text())  # self-install into repo
    if "--agent" in sys.argv:
        i = sys.argv.index("--file") + 1 if "--file" in sys.argv else None
        agent(sys.argv[i] if i else None)
    else:
        setup()
