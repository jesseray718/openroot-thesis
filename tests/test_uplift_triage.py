import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "code" / "python"
EXPECTED_WEAK = [12, 11, 13, 10, 14, 9]


def run_triage(script_name: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "python"
        shutil.copytree(SOURCE, work)

        completed = subprocess.run(
            [sys.executable, script_name],
            cwd=work,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            raise AssertionError(
                f"{script_name} failed:\nSTDOUT:\n{completed.stdout}\n"
                f"STDERR:\n{completed.stderr}"
            )

        return json.loads((work / "uplift_priority.json").read_text(encoding="utf-8"))


def ranked_hours(payload):
    if not isinstance(payload, list):
        raise AssertionError(
            f"Expected priority JSON list, got {type(payload).__name__}"
        )
    return [int(row["hour"]) for row in payload]


class UpliftTriageTests(unittest.TestCase):
    def test_triage2_and_triage3_match(self):
        triage2 = run_triage("uplift_triage2.py")
        triage3 = run_triage("uplift_triage3.py")
        self.assertEqual(triage2, triage3)

    def test_expected_weak_nodes_are_selected(self):
        result = run_triage("uplift_triage3.py")
        self.assertEqual(ranked_hours(result)[:6], EXPECTED_WEAK)
        self.assertEqual(len(result), 24)


if __name__ == "__main__":
    unittest.main()
