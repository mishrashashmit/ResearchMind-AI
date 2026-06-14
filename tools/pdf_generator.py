"""PDF generation utilities for ResearchMind AI using ReportLab (FIXED OVERLAP VERSION)."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, grey
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from config import Config, logger


# =========================
# DOCUMENT CREATION
# =========================

def create_pdf_document(output_path: str | Path, title: str, page_size: str = "letter"):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    return SimpleDocTemplate(
        str(output_path),
        pagesize=A4 if page_size.lower() == "a4" else letter,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title=title,
    )


# =========================
# STYLES (FIXED LINE HEIGHT)
# =========================

def get_custom_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["title"] = ParagraphStyle(
        "title",
        parent=base["Heading1"],
        fontSize=22,
        textColor=HexColor("#1f77b4"),
        alignment=1,
        spaceAfter=18,
        leading=26,   # FIX
    )

    styles["heading1"] = ParagraphStyle(
        "heading1",
        parent=base["Heading1"],
        fontSize=14,
        textColor=HexColor("#1f77b4"),
        spaceBefore=10,
        spaceAfter=8,
        leading=18,
    )

    styles["heading2"] = ParagraphStyle(
        "heading2",
        parent=base["Heading2"],
        fontSize=12,
        textColor=HexColor("#ff7f0e"),
        spaceBefore=6,
        spaceAfter=6,
        leading=16,
    )

    styles["body"] = ParagraphStyle(
        "body",
        parent=base["BodyText"],
        fontSize=10,
        leading=14,   # FIX: prevents overlap
        spaceAfter=6,
    )

    styles["footer"] = ParagraphStyle(
        "footer",
        parent=base["Normal"],
        fontSize=8,
        textColor=grey,
        alignment=2,
        leading=10,
    )

    return styles


# =========================
# SAFE TEXT WRAPPER (IMPORTANT FIX)
# =========================

def safe_para(text: str) -> Paragraph:
    """Prevents overflow issues inside tables."""
    text = str(text).replace("\n", " ").strip()
    return Paragraph(text, getSampleStyleSheet()["BodyText"])


# =========================
# TABLE FIX (MAIN OVERLAP FIX)
# =========================

def format_paper_table_data(papers: List[Dict[str, Any]]):
    table_data = [[
        Paragraph("<b>Title</b>", getSampleStyleSheet()["BodyText"]),
        Paragraph("<b>Summary</b>", getSampleStyleSheet()["BodyText"]),
        Paragraph("<b>Topics</b>", getSampleStyleSheet()["BodyText"]),
    ]]

    for paper in papers:
        title = str(paper.get("title", "N/A"))[:80]
        summary = str(paper.get("summary", "N/A"))[:200]
        topics = ", ".join(paper.get("topics", []))[:80]

        table_data.append([
            safe_para(title),
            safe_para(summary),
            safe_para(topics),
        ])

    col_widths = [2.0 * inch, 3.0 * inch, 1.8 * inch]

    return table_data, col_widths


def apply_table_style(table: Table):
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1f77b4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),

        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        # 🔥 FIX: spacing to avoid overlap
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f5f5f5")]),
        ("GRID", (0, 0), (-1, -1), 0.5, grey),

        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    return table


# =========================
# MAIN REPORT FUNCTION
# =========================

def generate_research_report(topic, papers, emerging_trends, filename="report.pdf"):
    output_path = Path(Config.REPORTS_DIR) / filename
    doc = create_pdf_document(output_path, "Research Report")
    styles = get_custom_styles()

    story = []

    story.append(Paragraph("ResearchMind AI Report", styles["title"]))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph(f"<b>Topic:</b> {topic}", styles["body"]))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.now()}", styles["body"]))
    story.append(Spacer(1, 0.2 * inch))

    # Trends
    if emerging_trends:
        story.append(Paragraph("Emerging Trends", styles["heading1"]))
        story.append(Paragraph(", ".join(emerging_trends), styles["body"]))
        story.append(Spacer(1, 0.2 * inch))

    # Table
    story.append(Paragraph("Papers", styles["heading1"]))

    table_data, col_widths = format_paper_table_data(papers)
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table = apply_table_style(table)

    story.append(table)

    doc.build(story)

    return str(output_path)



def generate_detailed_analysis_report(
    topic,
    papers,
    emerging_trends,
    filename="detailed_report.pdf"
):
    """
    Generates a detailed research report.

    Currently extends the standard report generation.
    You can later customize this with additional sections,
    paper-by-paper analysis, statistics, charts, etc.
    """

    output_path = Path(Config.REPORTS_DIR) / filename
    doc = create_pdf_document(output_path, "Detailed Research Report")
    styles = get_custom_styles()

    story = []

    # Title
    story.append(Paragraph("ResearchMind AI - Detailed Analysis Report", styles["title"]))
    story.append(Spacer(1, 0.2 * inch))

    # Metadata
    story.append(Paragraph(f"<b>Topic:</b> {topic}", styles["body"]))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.now()}", styles["body"]))
    story.append(Spacer(1, 0.2 * inch))

    # Trends Section
    story.append(Paragraph("Emerging Trends", styles["heading1"]))

    if emerging_trends:
        for trend in emerging_trends:
            story.append(Paragraph(f"• {trend}", styles["body"]))
    else:
        story.append(Paragraph("No trends identified.", styles["body"]))

    story.append(Spacer(1, 0.2 * inch))

    # Detailed Paper Analysis
    story.append(Paragraph("Paper Analysis", styles["heading1"]))

    for idx, paper in enumerate(papers, start=1):
        story.append(
            Paragraph(
                f"{idx}. {paper.get('title', 'Untitled')}",
                styles["heading2"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Summary:</b> {paper.get('summary', 'N/A')}",
                styles["body"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Topics:</b> {', '.join(paper.get('topics', []))}",
                styles["body"]
            )
        )

        story.append(Spacer(1, 0.1 * inch))

    doc.build(story)

    return str(output_path)



# =========================
# TEST
# =========================

if __name__ == "__main__":
    test_papers = [
        {
            "title": "Attention is All You Need",
            "summary": "Transformer architecture introduces self-attention mechanism for NLP tasks",
            "topics": ["Transformers", "Attention", "NLP"]
        },
        {
            "title": "BERT Model",
            "summary": "Bidirectional encoder representations for language understanding",
            "topics": ["BERT", "NLP", "Pretraining"]
        }
    ]

    path = generate_research_report(
        "NLP",
        test_papers,
        ["Transformers", "LLMs", "Attention Mechanism"],
        "fixed_report.pdf"
    )

    print("Generated:", path)