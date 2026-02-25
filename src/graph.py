"""Partial StateGraph wiring for interim: run detectives in parallel, aggregate evidence.

This module provides a minimal runner that implements the fan-out (detectives)
and a fan-in aggregator. It intentionally avoids requiring LangGraph to run,
so you can run an interim local check quickly.
"""
from typing import List

from src.nodes.detectives import run_detectives_parallel
from src.state import Evidence


def EvidenceAggregator(evidences: List[Evidence]) -> dict:
    """Simple aggregator: group by goal and return counts."""
    agg = {}
    for e in evidences:
        agg.setdefault(e.goal, []).append(e.dict())
    return {"by_goal": agg, "total_evidences": len(evidences)}


def run_interim_detection(repo_path: str, pdf_path: str, dimension_id: str = "git_forensic_analysis") -> dict:
    evidences = run_detectives_parallel(repo_path, pdf_path, dimension_id)
    aggregated = EvidenceAggregator(evidences)
    return {"evidences": [e.dict() for e in evidences], "aggregated": aggregated}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python src/graph.py <repo_path> <pdf_path>")
        sys.exit(1)
    repo_path = sys.argv[1]
    pdf_path = sys.argv[2]
    out = run_interim_detection(repo_path, pdf_path)
    import json
    print(json.dumps(out, indent=2))
