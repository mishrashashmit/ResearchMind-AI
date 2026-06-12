"""ResearchMind AI - Multi-Agent Research Assistant Package."""

__version__ = "1.0.0"
__author__ = "ResearchMind Team"
__description__ = "Multi-agent research assistant that searches papers, summarizes them, and generates reports"

# Make agents and tools importable from package root
from agents import search_agent, summary_agent, topic_agent, trend_agent
from tools import paper_counter, pdf_generator

__all__ = [
    "search_agent",
    "summary_agent",
    "topic_agent",
    "trend_agent",
    "paper_counter",
    "pdf_generator",
]
