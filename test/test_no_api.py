from tools.paper_counter import count_papers, calculate_paper_statistics
from tools.pdf_generator import get_custom_styles, format_paper_table_data

print("\n----LOCAL LOGIC TEST----n")

test_papers = [
    {"title": "P1", "summary": "S1", "topics": ["AI", "ML"]},
    {"title": "P2", "summary": "S2", "topics": ["AI", "NLP"]},
    {"title": "P3", "summary": "S3", "topics": ["CV"]},
]

# Paper counter test
count = count_papers(test_papers)
stats = calculate_paper_statistics(test_papers)

print("Paper Counter:")
print("Total:", count)
print("Unique Topics:", stats["unique_topics"])
print("Top Topic:", stats["most_common_topics"])

# PDF utilities test
styles = get_custom_styles()
table_data, widths = format_paper_table_data(test_papers)

print("\nPDF Module:")
print("Styles:", len(styles))
print("Table rows:", len(table_data))

print("\n----ALL LOCAL TESTS PASSED----")