"""Module functionality test."""

from tools.paper_counter import count_papers, calculate_paper_statistics
from tools.pdf_generator import get_custom_styles, format_paper_table_data

print("\n" + "=" * 70)
print("  Testing Individual Module Functionality")
print("=" * 70 + "\n")

test_papers = [
    {"title": "P1", "summary": "S1", "topics": ["AI", "ML"]},
    {"title": "P2", "summary": "S2", "topics": ["AI", "NLP"]},
    {"title": "P3", "summary": "S3", "topics": ["CV"]},
]

count = count_papers(test_papers)
stats = calculate_paper_statistics(test_papers)

print("📊 Paper Counter Module:")
print(f"  ✓ Total papers: {count}")
print(f"  ✓ Unique topics: {stats['unique_topics']}")
print(f"  ✓ Most common: {stats['most_common_topics'][0]}")
print()

styles = get_custom_styles()
print("📄 PDF Generator Module:")
print(f"  ✓ Custom styles created: {len(styles)} styles")
print(f"  ✓ Available styles: {list(styles.keys())}")

table_data, widths = format_paper_table_data(test_papers)
print(f"  ✓ Table formatting: {len(table_data)} rows, {len(widths)} columns")
print()

print("🤖 Agent Modules:")
from agents.search_agent import initialize_gemini as search_init
from agents.summary_agent import initialize_gemini as summary_init
from agents.topic_agent import initialize_gemini as topic_init
from agents.trend_agent import initialize_gemini as trend_init

print("  ✓ search_agent module loaded")
print("  ✓ summary_agent module loaded")
print("  ✓ topic_agent module loaded")
print("  ✓ trend_agent module loaded")
print()

print("✅ All module functionality tests passed!")
