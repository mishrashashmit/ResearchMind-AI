"""
Topic Agent for ResearchMind AI.

Extracts major research themes and topics from paper summaries using Gemini 2.5.
Optimized version (BATCH PROCESSING - 1 API call only).
"""

import json
from typing import Any, Dict, List

from google import genai
from config import Config, logger


# =========================
# GEMINI INITIALIZATION
# =========================
def initialize_gemini():
    """Initialize Gemini client."""
    if not Config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set. Please set it in .env file.")

    logger.info("Gemini API initialized for topic agent")
    return genai.Client(api_key=Config.GEMINI_API_KEY)


# =========================
# CLEAN RESPONSE
# =========================
def _clean_json(text: str) -> str:
    """Remove markdown formatting from Gemini response."""
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return text


# =========================
# BATCH TOPIC EXTRACTION (MAIN FUNCTION)
# =========================
def extract_topics_from_papers(
    papers: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Extract topics for ALL papers in ONE Gemini call.
    """

    if not isinstance(papers, list):
        raise ValueError("Papers must be a list")

    if len(papers) == 0:
        logger.warning("Empty papers list received for topic extraction")
        return []

    try:
        client = initialize_gemini()

        # ---------------- FORMAT INPUT ----------------
        formatted_papers = []

        for i, p in enumerate(papers, 1):
            title = p.get("title", "").strip()
            summary = p.get("summary", "").strip()

            if not title or not summary:
                continue

            formatted_papers.append(
                f"""
Paper {i}
Title: {title}
Summary: {summary}
"""
            )

        if not formatted_papers:
            logger.warning("No valid papers found for topic extraction")
            return []

        # ---------------- PROMPT ----------------
        prompt = f"""
You are an AI research assistant.

Extract 3–7 key research topics for EACH paper.

Return ONLY valid JSON:

{{
  "results": [
    {{
      "paper_index": 1,
      "topics": ["Topic1", "Topic2"]
    }},
    {{
      "paper_index": 2,
      "topics": ["Topic1", "Topic2"]
    }}
  ]
}}

Rules:
- 2–3 words per topic
- No explanation
- Strict JSON only

PAPERS:
{chr(10).join(formatted_papers)}
"""

        logger.info(f"Sending {len(formatted_papers)} papers to Gemini for topic extraction")

        # ---------------- GEMINI CALL ----------------
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            logger.warning("Empty response from Gemini for topics")
            return []

        # ---------------- PARSE RESPONSE ----------------
        text = _clean_json(response.text)

        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            logger.error("Failed to parse Gemini JSON response")
            return []

        # ---------------- BUILD OUTPUT ----------------
        enriched = []

        for p in papers:
            enriched.append({**p, "topics": []})

        for item in result.get("results", []):
            idx = item.get("paper_index", 1) - 1

            if 0 <= idx < len(enriched):
                enriched[idx]["topics"] = item.get("topics", [])

        logger.info(f"Topic extraction completed for {len(enriched)} papers")

        return enriched

    except Exception as e:
        logger.error(f"Topic extraction failed: {str(e)}")
        return []


# =========================
# GET ALL UNIQUE TOPICS
# =========================
def get_all_topics(papers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract unique topics from all papers."""

    unique_topics = set()

    for paper in papers:
        if not isinstance(paper, dict):
            continue

        for t in paper.get("topics", []):
            if isinstance(t, str):
                unique_topics.add(t.strip())

    sorted_topics = sorted(unique_topics)

    return {
        "topics": sorted_topics,
        "total_unique_topics": len(sorted_topics),
    }


# =========================
# TEST BLOCK
# =========================
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Topic Agent (OPTIMIZED BATCH VERSION)")
    print("=" * 60)

    test_papers = [
        {
            "title": "RAG Systems for Knowledge Retrieval",
            "summary": "Retrieval augmented generation improves LLM factuality.",
            "year": 2024,
        },
        {
            "title": "RLHF for Language Model Alignment",
            "summary": "Human feedback improves alignment using reinforcement learning.",
            "year": 2023,
        },
    ]

    result = extract_topics_from_papers(test_papers)

    print("\nRESULT:")
    for p in result:
        print(p["title"])
        print("Topics:", p["topics"])

    print("\nALL TOPICS:", get_all_topics(result))

    print("\nDONE")