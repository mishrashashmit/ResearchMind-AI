"""Trend Agent for ResearchMind AI.

Identifies emerging research trends and recurring ideas across multiple papers
using Gemini 2.5 API.
"""

import json
from typing import Any, Dict, List

from google import genai
from config import Config, logger


def initialize_gemini():
    """Initialize Gemini client."""

    if not Config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set. Please set it in .env file.")

    logger.info("Gemini API initialized for trend agent")

    return genai.Client(api_key=Config.GEMINI_API_KEY)


def _clean_json(text: str) -> str:
    """Clean Gemini markdown output."""
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return text


def identify_trends(
    papers: List[Dict[str, Any]]
) -> Dict[str, Any]:

    if not isinstance(papers, list):
        raise ValueError("Papers must be a list")

    if len(papers) < 2:
        raise ValueError("Need at least 2 papers to identify trends")

    try:
        client = initialize_gemini()

        papers_text = ""

        for idx, paper in enumerate(papers, 1):
            if not isinstance(paper, dict):
                continue

            title = paper.get("title", "Unknown")
            summary = paper.get("summary", "")
            topics = paper.get("topics", [])

            topics_str = ", ".join(topics) if isinstance(topics, list) else "N/A"

            papers_text += f"""
Paper {idx}: {title}
Summary: {summary}
Topics: {topics_str}
------------------------
"""

        prompt = f"""
Analyze these research papers and identify emerging trends.

{papers_text}

Return ONLY valid JSON:

{{
  "trends": ["Trend1", "Trend2", "Trend3"],
  "analysis": "2-3 sentence explanation"
}}

Rules:
- 4 to 8 trends
- Focus on emerging research directions
- No extra text
"""

        logger.info(f"Analyzing trends across {len(papers)} papers...")

        # ✅ GEMINI 2.5 CALL
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            raise Exception("Empty response from Gemini")

        response_text = _clean_json(response.text)

        result = json.loads(response_text)

        trends = result.get("trends", [])

        cleaned_trends = [
            str(t).strip()
            for t in trends
            if isinstance(t, str) and t.strip()
        ]

        return {
            "trends": cleaned_trends,
            "total_trends": len(cleaned_trends),
            "analysis": result.get("analysis", "")
        }

    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        raise Exception("Invalid JSON from Gemini")

    except Exception as e:
        logger.error(f"Error identifying trends: {e}")
        raise


def analyze_trend_frequency(
    papers: List[Dict[str, Any]]
) -> Dict[str, Any]:

    if not isinstance(papers, list) or len(papers) == 0:
        return {
            "frequent_topics": [],
            "weak_signals": [],
            "dominant_areas": []
        }

    topic_counts: Dict[str, int] = {}

    for paper in papers:
        if isinstance(paper, dict):
            topics = paper.get("topics", [])
            if isinstance(topics, list):
                for topic in topics:
                    if isinstance(topic, str):
                        topic_counts[topic] = topic_counts.get(topic, 0) + 1

    sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)

    frequent_topics = [
        {"topic": t, "count": c}
        for t, c in sorted_topics
    ]

    threshold = len(papers) * 0.4

    dominant_areas = [t for t, c in sorted_topics if c >= threshold]
    weak_signals = [t for t, c in sorted_topics if c == 1]

    return {
        "frequent_topics": frequent_topics,
        "weak_signals": weak_signals,
        "dominant_areas": dominant_areas
    }


def get_trend_report(
    papers: List[Dict[str, Any]]
) -> Dict[str, Any]:

    if len(papers) < 2:
        return {
            "trends": [],
            "total_trends": 0,
            "analysis": (
                "Hey buddy! You need at least 2 papers to identify trends. "
                "This topic currently has only 1 paper available, "
                "but don’t worry, we can still analyze summaries, topics, and generate the report."
            )
        }

    trends_result = identify_trends(papers)
    frequency_result = analyze_trend_frequency(papers)

    summary = (
        f"Analysis of {len(papers)} papers identified "
        f"{trends_result['total_trends']} trends. "
        f"{len(frequency_result['dominant_areas'])} dominant areas found. "
        f"{trends_result['analysis']}"
    )

    return {
        "emerging_trends": trends_result["trends"],
        "total_trends": trends_result["total_trends"],
        "frequency_analysis": frequency_result,
        "report_summary": summary
    }


# =========================
# TEST BLOCK
# =========================
if __name__ == "__main__":

    print("=" * 60)
    print("Testing Trend Agent (Gemini 2.5 FIXED)")
    print("=" * 60)

    test_papers = [
        {
            "title": "Agents and Tool Calling Systems",
            "summary": "Agentic AI with tool usage.",
            "topics": ["Agentic AI", "Tool Calling"],
        },
        {
            "title": "Reasoning in LLMs",
            "summary": "Improving reasoning capabilities.",
            "topics": ["Reasoning Models", "LLMs"],
        },
        {
            "title": "Multi-Agent Systems",
            "summary": "Collaborative AI frameworks.",
            "topics": ["Multi-Agent Systems", "Planning"],
        },
    ]

    print("\nIdentifying trends...")

    result = identify_trends(test_papers)

    print("\nTrends:")
    for i, t in enumerate(result["trends"], 1):
        print(f"{i}. {t}")

    print("\nAnalysis:", result["analysis"])

    print("\nTrend frequency:")
    freq = analyze_trend_frequency(test_papers)

    for item in freq["frequent_topics"]:
        print(item)

    print("\n✅ SUCCESS")