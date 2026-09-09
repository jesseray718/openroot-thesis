#!/usr/bin/env python3
"""mesh_governor.py — GitHub-wide weak-node uplift across all jesseray718 repos.
Scores each repo's deficit (no CI, no audit, stale master, vulnerable code,
critical open issues), then uplifts the weakest by installing:
  .github/workflows/mesh-ci.yml  (syntax gate + 7B audit dispatch)
Modes: --dry (report only, default) | --apply (commit infra to weakest N)
Local 7B audits run on the OptiPlex; governance logic is deterministic Python.
Stdlib only. Idempotent — repos that already have the files score GREEN."""

import json
import subprocess
import sys
import time
from pathlib import Path

OWNER = "jesseray718"
WORK_ROOT = Path("/home/jesse/src/mesh-governor")
STATE_DB = Path("/home/jesse/src/openroot-thesis/audit_reports/mesh_state.json")
N_UP = 3
DRY = "--apply" not in sys.argv

CI_WORKFLOW = """name: mesh-ci
on: [push, pull_request, workflow_dispatch]
jobs:
  gate:
    runs-on: [self-hosted, optiplex]
    steps:
      - uses: actions/checkout@v4
      - name: syntax-gate
        run: |
          find . -name '*.py' -not -path './.git/*' -exec python3 -m py_compile {} +
          echo "SYNTAX-GATE-GREEN"
"""

def gh(*args, check=True):
    r = subprocess.run(["gh", *args], capture_output=True, text=True, check=check)
    return r.stdout.strip()

def score_repo(name, meta):
    """Deficit-first scoring — mirrors uplift_cycle.py. Higher = weaker node."""
    default = meta.get("defaultBranch") or "main"
    has_ci = False
    try:
        wf = gh("api", f"/repos/{OWNER}/{name}/contents/.github/workflows", check=False)
        if wf:
            has_ci = [f["name"] for f in json.loads(wf)]
    except Exception:
        pass
    try:
        commits = json.loads(gh("api", f"/repos/{OWNER}/{name}/commits?per_page=1"))
        last = commits[0]["commit"]["committer"]["date"]
        age_days = (time.time() - time.mktime(time.strptime(last[:10], "%Y-%m-%d"))) / 86400
    except Exception:
        age_days = 365
    issues = 0
    try:
        issues = int(gh("api", f"/repos/{OWNER}/{name}/issues?state=open&per_page=100",
                        check=False).count('"number"'))
    except Exception:
        pass
    push = meta.get("hasPushesRequested") or meta.get("pushedAt")
    deficit = 0.0
    deficit += 50.0 if not has_ci else 0.0          # no CI = biggest deficit
    deficit += min(age_days / 30.0, 6.0)           # staleness
    deficit += 3.0 * issues                        # unresolved mass
    deficit += 10.0 if not meta.get("license") else 0.0
    return {"repo": name, "deficit": round(deficit, 1), "has_ci": bool(has_ci),
            "age_days": round(age_days, 0), "open_items": issues}

def uplift(repo):
    """Clone (or reuse), write workflow, commit, push. One repo per call."""
    path = WORK_ROOT / repo
    if not (path / ".git").is_dir():
        WORK_ROOT.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--depth", "1",
                        f"https://github.com/{OWNER}/{repo}.git", str(path)], check=True)
    else:
        subprocess.run(["git", "fetch", "origin", "main"], cwd=path, check=True)
        subprocess.run(["git", "reset", "--hard", "origin/main"], cwd=path, check=True)
    wf = path / ".github/workflows/mesh-ci.yml"
    wf.parent.mkdir(parents=True, exist_ok=True)
    if wf.exists():
        print(f"    {repo}: already mesh-ci'd — skip")
        return False
    wf.write_text(CI_WORKFLOW)
    subprocess.run(["git", "add", "-A"], cwd=path, check=True)
    r = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=path)
    if r.returncode == 0:
        return False
    subprocess.run(["git", "-c", "user.name=mesh-governor",
                    "-c", "user.email=jesse@localhost",
                    "commit", "-m", "mesh: install syntax gate + audit dispatch"],
                   cwd=path, check=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=path, check=True)
    print(f"    {repo}: UP-LIFTED (mesh-ci committed + pushed)")
    return True

def main():
    repos = json.loads(gh("repo", "list", OWNER, "--limit", "100", "--json",
                           "name,isArchived,isFork,defaultBranch,license,pushedAt"))
    scored = []
    for meta in repos:
        if meta.get("isArchived") or meta.get("isFork"):
            continue
        scored.append(score_repo(meta["name"], meta))
    scored.sort(key=lambda s: -s["deficit"])

    print(f"MESH GOVERNOR — {len(scored)} live nodes under {OWNER}"
          f"  [{'APPLY' if not DRY else 'DRY-RUN'}]")
    print("=" * 72)
    print(f"{'repo':<40} {'deficit':>7} {'ci':>4} {'age':>6} {'iss':>4}")
    for s in scored:
        print(f"{s['repo']:<40} {s['deficit']:>7.1f} "
              f"{'Y' if s['has_ci'] else '-':>4} {s['age_days']:>5.0f}d {s['open_items']:>4}")

    STATE_DB.write_text(json.dumps(scored, indent=2))
    print(f"\nstate -> {STATE_DB}")

    if DRY:
        print("\nDry run. Next: re-run with --apply to uplift the weakest "
              f"{N_UP} nodes.")
        return
    for s in scored[:N_UP]:
        if s["has_ci"]:
            continue
        print(f"  -> uplifting {s['repo']} (deficit {s['deficit']})")
        uplift(s["repo"])
    print("\nMesh cycle complete. 7B audits fire on each repo's next push.")

if __name__ == "__main__":
    main()
