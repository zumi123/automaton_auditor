import ast
import os
import subprocess
import tempfile
from typing import Dict, List, Optional


def clone_repo(git_url: str, timeout: int = 60) -> Optional[str]:
    """Clone a repo into a temporary directory and return the path.

    Uses tempfile.TemporaryDirectory semantics; caller should copy or read
    contents before the directory is removed.
    """
    temp_dir = tempfile.mkdtemp(prefix="auditor_repo_")
    try:
        res = subprocess.run(
            ["git", "clone", "--depth", "50", git_url, temp_dir],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if res.returncode != 0:
            raise RuntimeError(f"git clone failed: {res.stderr.strip()}")
        return temp_dir
    except Exception:
        # Caller should handle None as clone failure
        return None


def extract_git_history(repo_path: str) -> List[Dict]:
    """Run `git log --oneline --reverse` and return list of commits with timestamp.

    repo_path: path to cloned repo
    returns: list of dicts {message, hash}
    """
    try:
        res = subprocess.run(
            ["git", "log", "--pretty=format:%H|%cI|%s", "--reverse"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode != 0:
            return []
        lines = res.stdout.splitlines()
        commits = []
        for ln in lines:
            parts = ln.split("|", 2)
            if len(parts) == 3:
                commits.append({"hash": parts[0], "timestamp": parts[1], "message": parts[2]})
        return commits
    except Exception:
        return []


def analyze_graph_structure(repo_path: str) -> Dict:
    """Basic AST-based analysis to find StateGraph instantiation and builder edges.

    This function is intentionally conservative: it parses Python files and
    searches for:
      - ast.Name or ast.Attribute nodes with id 'StateGraph'
      - function calls named 'add_edge' or attribute calls like builder.add_edge

    Returns a dict summarizing findings and example source snippets.
    """
    findings = {"stategraph_found": False, "edges": [], "snippets": []}
    for root, dirs, files in os.walk(repo_path):
        for fn in files:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(root, fn)
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    src = fh.read()
                tree = ast.parse(src)
            except Exception:
                continue

            # Look for Name/Attribute nodes referencing 'StateGraph'
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    # function name
                    func = node.func
                    func_name = None
                    if isinstance(func, ast.Attribute):
                        func_name = func.attr
                    elif isinstance(func, ast.Name):
                        func_name = func.id
                    if func_name == "add_edge":
                        findings["edges"].append({"file": path, "lineno": node.lineno})
                        snippet = _extract_snippet(src, node.lineno)
                        findings["snippets"].append(snippet)
                if isinstance(node, ast.Name) and node.id == "StateGraph":
                    findings["stategraph_found"] = True
                if isinstance(node, ast.Attribute) and getattr(node, "attr", None) == "StateGraph":
                    findings["stategraph_found"] = True

    return findings


def _extract_snippet(src: str, lineno: int, context: int = 4) -> str:
    lines = src.splitlines()
    start = max(0, lineno - context - 1)
    end = min(len(lines), lineno + context)
    return "\n".join(lines[start:end])
