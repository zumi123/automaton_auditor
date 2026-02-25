from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

from ..state import Evidence
from ..tools import repo_tools, doc_tools


def RepoInvestigator(repo_path: str, dimension_id: str) -> Evidence:
    """Collect forensic evidence about the repo for a single dimension.

    Returns an `Evidence` model instance (as dict-like object for now).
    """
    commits = repo_tools.extract_git_history(repo_path)
    findings = repo_tools.analyze_graph_structure(repo_path)

    found = bool(commits or findings.get("stategraph_found"))
    content = None
    if findings.get("snippets"):
        content = findings["snippets"][0]

    return Evidence(
        goal=dimension_id,
        found=found,
        content=content,
        location=repo_path,
        rationale=f"Found {len(commits)} commits; stategraph_found={findings.get('stategraph_found')}",
        confidence=0.9 if found else 0.1,
    )


def DocAnalyst(pdf_path: str, dimension_id: str) -> Evidence:
    chunks = doc_tools.ingest_pdf(pdf_path)
    paths = []
    if chunks:
        joined = "\n".join(chunks)
        paths = doc_tools.extract_file_paths_from_text(joined)

    found = bool(paths)
    return Evidence(
        goal=dimension_id,
        found=found,
        content=(";".join(paths)) if paths else None,
        location=pdf_path,
        rationale=f"Extracted {len(paths)} file paths from PDF",
        confidence=0.8 if found else 0.2,
    )


def run_detectives_parallel(repo_path: str, pdf_path: str, dimension_id: str) -> List[Evidence]:
    """Run detectives in parallel and return aggregated Evidence objects."""
    results = []
    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = [ex.submit(RepoInvestigator, repo_path, dimension_id), ex.submit(DocAnalyst, pdf_path, dimension_id)]
        for f in futures:
            try:
                results.append(f.result())
            except Exception:
                pass
    return results
