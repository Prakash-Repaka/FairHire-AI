from __future__ import annotations

from io import BytesIO
from typing import Any

from fastapi import HTTPException, status

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except Exception:  # noqa: BLE001
    canvas = None
    letter = None


def build_report_pdf(report: dict[str, Any]) -> bytes:
    if canvas is None or letter is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='PDF export is unavailable until reportlab is installed.')

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    def write_line(text: str, x: int = 50, y: int = 760, size: int = 12) -> None:
        pdf.setFont('Helvetica', size)
        pdf.drawString(x, y, text)

    pdf.setTitle('FairHire AI Board Report')
    write_line('FairHire AI Board-Ready Report', 50, 760, 18)
    write_line(f"Run ID: {report.get('run_id', 'unknown')}", 50, 734, 11)

    y = 700
    sections = [
        ('Summary', f"Accuracy: {report.get('train', {}).get('accuracy', 0):.2f} | Fairness: {report.get('bias', {}).get('fairness_index', 0):.2f}"),
        ('Risk Areas', f"Parity gap: {report.get('bias', {}).get('demographic_parity_difference', 0):.2f}"),
        ('Recommendations', 'Reweight dataset, remove proxy features, recalibrate threshold.'),
    ]
    for title, value in sections:
        write_line(title, 50, y, 14)
        y -= 18
        for line in _wrap_text(value, 90):
            write_line(line, 60, y, 11)
            y -= 14
        y -= 8

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer.read()


def _wrap_text(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = ' '.join(current + [word])
        if len(candidate) > width and current:
            lines.append(' '.join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(' '.join(current))
    return lines
