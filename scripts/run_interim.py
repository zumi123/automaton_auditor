#!/usr/bin/env python3
"""CLI: run the interim detector against a repository URL and a PDF report.

Usage:
    python3 scripts/run_interim.py <git_repo_url> <pdf_path>

The script clones the target repo into a temporary directory, runs the
interim detectives, writes a JSON result to `reports/interim_run.json`, and
prints the summary.
"""
import json
import sys
from pathlib import Path

from src.tools import repo_tools
from src.graph import run_interim_detection


def main(argv):
    if len(argv) < 3:
        print("Usage: run_interim.py <git_repo_url> <pdf_path>")
        return 2
    git_url = argv[1]
    pdf_path = argv[2]

    cloned = repo_tools.clone_repo(git_url)
    if not cloned:
        print("Failed to clone repository:", git_url)
        return 1

    out = run_interim_detection(cloned, pdf_path)

    out_path = Path('reports') / 'interim_run.json'
    out_path.write_text(json.dumps(out, indent=2))
    print("Wrote:", out_path)
    print("Summary:")
    print(json.dumps({'total_evidences': out.get('aggregated',{}).get('total_evidences',0)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
