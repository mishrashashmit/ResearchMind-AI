"""Summary Agent for ResearchMind AI.

Generates detailed summaries for research papers using Google Gemini API.
Enriches papers with comprehensive summaries while preserving original data.
"""

from typing import Any, Dict, List

from google import genai
from config import Config, logger


def initialize_gemini():
    """Initialize Gemini client with API key."""

    if not Config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set. Please set it in .env file.")

    logger.info("Gemini API initialized for summary agent")

    return genai.Client(api_key=Config.GEMINI_API_KEY)


def generate_detailed_summary(paper_title: str, brief_summary: str) -> str:
    """Generate a detailed summary for a single paper using Gemini API."""

    if not isinstance(paper_title, str) or not paper_title.strip():
        raise ValueError("Paper title must be a non-empty string")

    if not isinstance(brief_summary, str) or not brief_summary.strip():
        raise ValueError("Brief summary must be a non-empty string")

    try:
        client = initialize_gemini()

        prompt = f"""
Based on the following research paper information, create a detailed 2-3 paragraph summary.

Paper Title: {paper_title}
Brief Summary: {brief_summary}

Include:
1. Methodology
2. Key findings
3. Practical implications

Keep it clear and technical but readable.
"""

        logger.info(f"Generating summary for: {paper_title[:50]}...")

        # ✅ FIXED GEMINI 2.5 CALL
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            raise Exception("Empty response from Gemini API")

        summary = response.text.strip()

        if len(summary) < 50:
            return brief_summary

        return summary

    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise


def summarize_papers(papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate detailed summaries for a list of research papers."""

    if not isinstance(papers, list):
        raise ValueError("Papers must be a list of dictionaries")

    if len(papers) == 0:
        raise ValueError("Papers list cannot be empty")

    summarized_papers: List[Dict[str, Any]] = []

    for idx, paper in enumerate(papers, 1):
        try:
            if not isinstance(paper, dict):
                continue

            title = paper.get("title", "").strip()
            summary = paper.get("summary", "").strip()
            year = paper.get("year")

            if not title or not summary:
                continue

            logger.info(f"Processing {idx}/{len(papers)}: {title[:50]}...")

            detailed_summary = generate_detailed_summary(title, summary)

            summarized_papers.append({
                "title": title,
                "summary": summary,
                "year": year,
                "detailed_summary": detailed_summary,
            })

        except Exception as e:
            logger.error(f"Error in paper {idx}: {str(e)}")
            continue

    if not summarized_papers:
        raise Exception("Failed to summarize any papers")

    return summarized_papers


# =========================
# TEST BLOCK
# =========================
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Summary Agent (Gemini 2.5 FIXED)")
    print("=" * 60)

    test_papers = [
        {
            "title": "Attention is All You Need",
            "summary": "Introduces the Transformer architecture.",
            "year": 2017,
        },
        {
            "title": "BERT: Pre-training of Deep Bidirectional Transformers",
            "summary": "Bidirectional language model using masking.",
            "year": 2018,
        },
    ]

    try:
        print("\nInput papers:")
        for paper in test_papers:
            print(f"- {paper['title']}")

        print("\nGenerating summaries...")

        result = summarize_papers(test_papers)

        print(f"\n✓ Summarized {len(result)} papers\n")

        for i, p in enumerate(result, 1):
            print(f"Paper {i}")
            print("Title:", p["title"])
            print("Summary:", p["summary"][:80], "...")
            print("Detailed:", p["detailed_summary"][:120], "...")
            print()

        print("=" * 60)
        print("✅ SUCCESS")
        print("=" * 60)

    except Exception as e:
        print("❌ ERROR:", str(e))