"""LangGraph StateGraph wiring (interim).

This module attempts to build a LangGraph `StateGraph` when the `langgraph`
package is available. If not available, a safe fallback runs the existing
interim runner (`src.graph.run_interim_detection`) so you can still execute
the workflow locally.

To use the real LangGraph wiring, install the package (example):
    pip install langgraph

Note: the actual LangGraph API surface may differ; this file is an integration
point and can be adapted when the dependency is available in your environment.
"""
from typing import Optional
import logging

from pathlib import Path

from src.graph import run_interim_detection

try:
    import langgraph as lg  # type: ignore
    LANGGRAPH_AVAILABLE = True
except Exception:
    LANGGRAPH_AVAILABLE = False

logger = logging.getLogger(__name__)


def run_stategraph(repo_path: str, pdf_path: str, dimension_id: str = "git_forensic_analysis") -> dict:
    """Run either a LangGraph StateGraph (if available) or fallback runner.

    Returns a dict containing `evidences` and `aggregated` keys similar to
    the interim runner.
    """
    if not LANGGRAPH_AVAILABLE:
        logger.warning("langgraph not installed; running fallback interim runner")
        return run_interim_detection(repo_path, pdf_path, dimension_id)

    # Example LangGraph usage (pseudo-code). Adapt when the real API is known.
    # This section constructs a StateGraph with START/END, detectives fan-out,
    # an EvidenceAggregator fan-in, and conditional edges for missing evidence.
    try:
        builder = lg.StateGraph(name="AutomatonAuditorInterim")

        start = lg.Node("START")
        repo_node = lg.Node("RepoInvestigator", func=lambda s: None)
        doc_node = lg.Node("DocAnalyst", func=lambda s: None)
        aggregator = lg.Node("EvidenceAggregator", func=lambda s: None)
        end = lg.Node("END")

        builder.add_node(start)
        builder.add_nodes([repo_node, doc_node, aggregator, end])

        # fan-out from start to detectives
        builder.add_edge(start, repo_node)
        builder.add_edge(start, doc_node)

        # fan-in to aggregator
        builder.add_edge(repo_node, aggregator)
        builder.add_edge(doc_node, aggregator)

        # aggregator -> end
        builder.add_edge(aggregator, end)

        # execute graph (pseudo)
        result = builder.run(initial_state={"repo_path": repo_path, "pdf_path": pdf_path})
        return result
    except Exception as exc:
        logger.exception("LangGraph execution failed, falling back")
        return run_interim_detection(repo_path, pdf_path, dimension_id)
