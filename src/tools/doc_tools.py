import re
from typing import List

try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None


def ingest_pdf(path: str) -> List[str]:
    """Return a list of text chunks extracted from the PDF.

    If PyPDF2 is unavailable, returns an empty list.
    """
    if PdfReader is None:
        return []
    try:
        reader = PdfReader(path)
        pages = [p.extract_text() or "" for p in reader.pages]
        # very simple chunking: split by 1000 characters
        chunks = []
        for ptext in pages:
            for i in range(0, len(ptext), 1000):
                chunks.append(ptext[i : i + 1000])
        return chunks
    except Exception:
        return []


def extract_file_paths_from_text(text: str) -> List[str]:
    """Find likely repo file paths like 'src/...py' in text."""
    paths = re.findall(r"(src/[\w/\-_.]+\.py)", text)
    return list(dict.fromkeys(paths))


def extract_file_paths_from_pdf(path: str) -> List[str]:
    chunks = ingest_pdf(path)
    all_paths = []
    for c in chunks:
        all_paths.extend(extract_file_paths_from_text(c))
    return list(dict.fromkeys(all_paths))
