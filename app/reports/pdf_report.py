from __future__ import annotations

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def build_pdf_report(project_name: str, results: dict) -> bytes:
    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    quality = results["quality"]
    profile = results["profile"]
    duplicates = results["duplicates"]
    outliers = results["outliers"]
    pii = results["pii"]

    story = [
        Paragraph("DatasetGuard AI - Dataset Quality Audit", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Dataset: {project_name}", styles["Heading2"]),
        Paragraph(
            f"Quality score: {quality['score']}/100 (Grade {quality['grade']})",
            styles["Heading2"],
        ),
        Spacer(1, 8),
        Paragraph(
            f"Rows: {profile['rows']} | Columns: {profile['columns']} | "
            f"Missing rate: {profile['missing_rate']:.2%}",
            styles["BodyText"],
        ),
        Paragraph(
            f"Exact duplicate rows: {duplicates['duplicate_rows']} | "
            f"Outliers: {outliers['outlier_count']} | "
            f"Potential PII findings: {pii['finding_count']}",
            styles["BodyText"],
        ),
        Spacer(1, 12),
        Paragraph("Quality observations", styles["Heading2"]),
    ]

    reasons = quality["reasons"] or [
        "No major quality issues detected by the configured checks."
    ]
    for reason in reasons:
        story.append(Paragraph(f"• {reason}", styles["BodyText"]))

    document.build(story)
    return buffer.getvalue()
