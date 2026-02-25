Interim Automaton Auditor

This repository contains an interim scaffold for Week 2: The Automaton Auditor.
Quick start (local, interim):

1. Create a virtual environment and install pinned dependencies.
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
2. Run the interim detection runner against a local cloned repo path and a PDF path:

   python -m src.graph <repo_path> <pdf_path>
Run against a remote GitHub repo URL (cloned into a sandboxed temporary dir):

   python3 scripts/run_interim.py https://github.com/OWNER/REPO.git reports/interim_report.pdf
Notes:
- This interim submission scaffolds the required files: `src/state.py`, `src/tools/*`, `src/nodes/detectives.py`, and `src/graph.py` (partial wiring).
- Replace `reports/interim_report.pdf` with your PDF report for peer access.
- The full LangGraph-based judges and ChiefJustice synthesis are part of the final submission.
Files of interest:
- src/state.py  -- Pydantic models and `AgentState` TypedDict
- src/tools/repo_tools.py  -- sandboxed `git clone`, git history and AST helpers
- src/tools/doc_tools.py  -- PDF ingestion helpers
- src/nodes/detectives.py  -- RepoInvestigator and DocAnalyst (parallel runner)
- src/graph.py  -- partial wiring & interim runner
- src/graph_langgraph.py -- LangGraph wiring (attempts to use `langgraph`, falls back to interim runner)
- scripts/run_interim.py -- CLI to run the interim detector against remote repo URLs
Reproducibility and runtime:
- Python: requires Python 3.8 - 3.11 (see `pyproject.toml`).
- Use `requirements.txt` for pinned installs to ensure reproducible environments.
Next steps:
- Migrate the interim runner into a true LangGraph StateGraph (see `src/graph_langgraph.py`).
- Implement Judge nodes and the ChiefJustice synthesis engine as part of the final submission.
Interim Automaton Auditor

This repository contains an interim scaffold for Week 2: The Automaton Auditor.

Quick start (local, interim):

1. Create a virtual environment and install dependencies from `pyproject.toml`.

   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt  # or pip install pydantic PyPDF2

2. Run the interim detection runner against a local cloned repo path and a PDF path:

   python -m src.graph <repo_path> <pdf_path>

Notes:
- This interim submission scaffolds the required files: `src/state.py`, `src/tools/*`, `src/nodes/detectives.py`, and `src/graph.py` (partial wiring).
- Replace `reports/interim_report.pdf` with your PDF report for peer access.
- The full LangGraph-based judges and ChiefJustice synthesis are part of the final submission.

Files of interest:
- src/state.py  -- Pydantic models and `AgentState` TypedDict
- src/tools/repo_tools.py  -- sandboxed `git clone`, git history and AST helpers
- src/tools/doc_tools.py  -- PDF ingestion helpers
- src/nodes/detectives.py  -- RepoInvestigator and DocAnalyst (parallel runner)
- src/graph.py  -- partial wiring & interim runner
