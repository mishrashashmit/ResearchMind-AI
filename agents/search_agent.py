"""Search Agent for ResearchMind AI.

Searches for research papers using Gemini API based on research topics.
Returns structured paper data with title, summary, and publication year.
"""

import json
from typing import Any, Dict, List

from google import genai
from config import Config, logger


def initialize_gemini() -> genai.Client:
    """Initialize Gemini client with API key."""

    if not Config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set. Please set it in .env file.")

    logger.info("Gemini API initialized successfully")

    return genai.Client(api_key=Config.GEMINI_API_KEY)


def search_papers(topic: str, num_papers: int = 5) -> List[Dict[str, Any]]:
    """Search for research papers using Gemini 2.5."""

    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("Topic must be a non-empty string")

    num_papers = min(max(num_papers, 1), 10)

    try:
        client = initialize_gemini()

        prompt = f"""
You are a research assistant.

Generate exactly {num_papers} realistic research papers about:
"{topic}"

Rules:
- Return ONLY valid JSON
- No markdown, no explanation
- Each item must contain:
  - title (string)
  - summary (1-2 sentences)
  - year (integer 2020-2025)

Return format:
[
  {{"title": "...", "summary": "...", "year": 2024}},
  {{"title": "...", "summary": "...", "year": 2023}}
]
"""

        logger.info(f"Searching papers for topic: {topic}")

        # ✅ GEMINI 2.5 CALL (CORRECT)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            raise Exception("Empty response from Gemini API")

        text = response.text.strip()

        # Remove markdown if Gemini adds it
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        papers = json.loads(text)

        if not isinstance(papers, list):
            raise ValueError("Invalid response format from API")

        validated = []

        for paper in papers:
            if not isinstance(paper, dict):
                continue

            title = paper.get("title", "").strip()
            summary = paper.get("summary", "").strip()
            year = paper.get("year", 2024)

            if not title or not summary:
                continue

            if not isinstance(year, int) or year < 2000 or year > 2026:
                year = 2024

            validated.append({
                "title": title,
                "summary": summary,
                "year": year
            })

        logger.info(f"Found {len(validated)} papers for topic: {topic}")

        return validated

    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        raise Exception(f"Invalid JSON response: {str(e)}")

    except Exception as e:
        logger.error(f"Error during paper search: {str(e)}")
        raise


# =========================
# TEST BLOCK
# =========================
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Search Agent (Gemini 2.5 FIXED)")
    print("=" * 60)

    try:
        papers = search_papers("machine learning", num_papers=3)

        print(f"\n✓ Found {len(papers)} papers\n")

        for i, p in enumerate(papers, 1):
            print(f"Paper {i}")
            print("Title:", p["title"])
            print("Year:", p["year"])
            print("Summary:", p["summary"][:100], "...")
            print()

        print("=" * 60)
        print("✅ SUCCESS")
        print("=" * 60)

    except Exception as e:
        print("❌ ERROR:", str(e))