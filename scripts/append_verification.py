from pathlib import Path
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter


def build_appendix_text(found_keywords: dict, repo_files_exist: dict, chunks_count: int) -> str:
    lines = []
    lines.append('Automaton Auditor — Verification Appendix')
    lines.append('')
    lines.append('Summary:')
    lines.append(f'- Extracted PDF text chunks: {chunks_count}')
    lines.append('- Detected rubric keywords present in the report:')
    for k in sorted(found_keywords.keys()):
        snippet = found_keywords[k]
        snippet = snippet.replace('\n', ' ').strip()
        lines.append(f'  - {k}: ...{snippet[:180]}...')
    lines.append('')
    lines.append('Repository files present (verified in workspace):')
    for f, ok in repo_files_exist.items():
        lines.append(f'  - {f}: {"FOUND" if ok else "MISSING"}')
    lines.append('')
    lines.append('Recommendation:')
    lines.append('- Add explicit file path citations and small code snippets in the PDF for stronger cross-reference evidence.')
    lines.append('- Include `src/nodes/judges.py` and ChiefJustice details if implemented, or state as future work.')
    return '\n'.join(lines)


def make_appendix_pdf(text: str, out_path: Path):
    pdf = FPDF(unit='pt', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=40)
    # Use a core font with latin-1 compatibility and replace unsupported chars
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 20, 'Verification Appendix', ln=1)
    pdf.ln(4)
    pdf.set_font('Arial', size=10)
    for line in text.split('\n'):
        # replace em-dash and other problematic unicode with ascii approximations
        safe = line.replace('\u2014', '--').encode('latin-1', errors='replace').decode('latin-1')
        pdf.multi_cell(0, 12, safe)
    pdf.output(str(out_path))


def append_page_to_pdf(original_pdf: Path, appendix_pdf: Path, output_pdf: Path):
    reader_orig = PdfReader(str(original_pdf))
    reader_append = PdfReader(str(appendix_pdf))
    writer = PdfWriter()
    for p in reader_orig.pages:
        writer.add_page(p)
    for p in reader_append.pages:
        writer.add_page(p)
    with open(output_pdf, 'wb') as fw:
        writer.write(fw)


if __name__ == '__main__':
    import json
    import sys
    base = Path(__file__).resolve().parents[1]
    pdf = base / 'reports' / 'interim_report.pdf'
    out = base / 'reports' / 'interim_report_updated.pdf'
    appendix_tmp = base / 'reports' / 'interim_appendix.pdf'

    # load findings from a helper JSON if available
    findings_json = base / 'reports' / 'interim_findings.json'
    if findings_json.exists():
        data = json.loads(findings_json.read_text())
        found_keywords = data.get('found_keywords', {})
        repo_files_exist = data.get('repo_files_exist', {})
        chunks_count = data.get('chunks_count', 0)
    else:
        # minimal defaults
        found_keywords = {}
        repo_files_exist = {}
        chunks_count = 0

    text = build_appendix_text(found_keywords, repo_files_exist, chunks_count)
    make_appendix_pdf(text, appendix_tmp)
    append_page_to_pdf(pdf, appendix_tmp, out)
    print('Wrote', out)
