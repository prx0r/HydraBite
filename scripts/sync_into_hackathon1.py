#!/usr/bin/env python3
"""Copy the verified release into an existing prx0r/hackathon1 clone.

This is intentionally additive: it does not delete design-history files such as IDEAS*/dossiers.
"""
from pathlib import Path
import shutil
import sys

SRC = Path(__file__).resolve().parents[1]
if len(sys.argv) != 2:
    raise SystemExit("usage: python scripts/sync_into_hackathon1.py /path/to/hackathon1")
DST = Path(sys.argv[1]).resolve()
if not (DST / ".git").exists():
    raise SystemExit(f"not a git clone: {DST}")

files = [
    "README.md", "SUBMISSION_FINAL.md", "SUBMISSION_STORY.md", "PROPOSAL.md", "DEMO.md",
    "MCP_AGENT_WORKFLOW.md", "DATA_AND_RIGHTS.md", "FAIR.md", "SCORING_MATRIX.md",
    "VIDEO_SCRIPT.md", "FINAL_EXTERNAL_CHECKS.md", "PUBLIC_REPO_SYNC.md", "PREEXISTING.md",
    "NOTICE.md", "LICENSE", "CITATION.cff", "codemeta.json", ".zenodo.json", "pyproject.toml",
    "BUILD_CERTIFICATE.json",
]
dirs = ["patala_research_ci", "tests", "fixtures", "schemas", "examples", "scripts", "docs", "LICENSES", ".github"]

for rel in files:
    src = SRC / rel
    if src.exists():
        dst = DST / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

for rel in dirs:
    src = SRC / rel
    if not src.exists():
        continue
    dst = DST / rel
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

# Remove/replace the obsolete draft submission so evaluators cannot land on the old MCP claim.
(DST / "SUBMISSION.md").write_text(
    "# Submission\n\nThe current judge-facing form is [`SUBMISSION_FINAL.md`](SUBMISSION_FINAL.md).\n"
    "This replaces the earlier draft that incorrectly treated the hackathon MCP criterion as not applicable.\n",
    encoding="utf-8",
)
print(f"Synced verified release into {DST}")
