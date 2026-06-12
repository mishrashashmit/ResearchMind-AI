"""Comprehensive test suite for ResearchMind AI.

Tests all modules and pipeline components.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent))

from config import Config, logger, setup_logging
from tools.paper_counter import (
    count_papers,
    count_papers_by_topic,
    calculate_paper_statistics,
    get_trending_topics,
)
from tools.pdf_generator import (
    get_custom_styles,
    format_paper_table_data,
    generate_research_report,
    generate_detailed_analysis_report,
)
from main import ResearchAnalyzer


def print_section(title: str) -> None:
    """Print formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def print_test(name: str) -> None:
    """Print test name."""
    print(f"  🧪 {name}...", end=" ")


def test_config() -> bool:
    """Test configuration module."""
    print_section("TEST 1: Configuration Module")
    
    try:
        print_test("Config class loads correctly")
        assert Config.GOOGLE_MODEL == "gemini-1.5-flash"
        print("✓")
        
        print_test("Reports directory exists")
        Config.ensure_directories()
        assert Config.REPORTS_DIR.exists()
        print("✓")
        
        print_test("Logs directory exists")
        assert Config.LOGS_DIR.exists()
        print("✓")
        
        print_test("Logger initialized")
        assert logger is not None
        print("✓")
        
        print("\n  ✅ Configuration tests passed!\n")
        return True
    
    except Exception as e:
        print(f"✗\n  ❌ Config test failed: {str(e)}\n")
        return False


def test_paper_counter() -> bool:
    """Test paper counter utilities."""
    print_section("TEST 2: Paper Counter Module")
    
    test_papers = [
        {"title": "Paper 1", "summary": "Short summary", "topics": ["AI", "ML"]},
        {"title": "Paper 2", "summary": "Another summary", "topics": ["AI", "NLP"]},
        {"title": "Paper 3", "summary": "Third summary", "topics": ["CV"]},
    ]
    
    try:
        print_test("count_papers()")
        count = count_papers(test_papers)
        assert count == 3, f"Expected 3, got {count}"
        print("✓")
        
        print_test("count_papers_by_topic()")
        by_topic = count_papers_by_topic(test_papers)
        assert by_topic["AI"] == 2, f"Expected AI count 2, got {by_topic['AI']}"
        assert by_topic["ML"] == 1
        print("✓")
        
        print_test("calculate_paper_statistics()")
        stats = calculate_paper_statistics(test_papers)
        assert stats["total_papers"] == 3
        assert stats["unique_topics"] == 4
        print("✓")
        
        print_test("get_trending_topics()")
        trending = get_trending_topics(test_papers, min_occurrences=2)
        assert len(trending) == 1
        assert trending[0]["topic"] == "AI"
        print("✓")
        
        print("\n  ✅ Paper Counter tests passed!\n")
        return True
    
    except Exception as e:
        print(f"✗\n  ❌ Paper Counter test failed: {str(e)}\n")
        return False


def test_pdf_generator() -> bool:
    """Test PDF generation."""
    print_section("TEST 3: PDF Generator Module")
    
    test_papers = [
        {
            "title": "AI Paper 1",
            "summary": "About artificial intelligence",
            "detailed_summary": "Comprehensive explanation about AI systems",
            "year": 2024,
            "topics": ["AI", "ML", "Deep Learning"],
        },
        {
            "title": "NLP Paper",
            "summary": "Natural language processing",
            "detailed_summary": "Advanced NLP techniques and models",
            "year": 2023,
            "topics": ["NLP", "Transformers", "Language Models"],
        },
    ]
    
    test_trends = ["AI Systems", "Deep Learning", "Neural Networks"]
    
    try:
        print_test("get_custom_styles()")
        styles = get_custom_styles()
        assert len(styles) == 5
        assert "title" in styles
        print("✓")
        
        print_test("format_paper_table_data()")
        table_data, col_widths = format_paper_table_data(test_papers)
        assert len(table_data) == 3  # header + 2 papers
        assert len(col_widths) == 3
        print("✓")
        
        print_test("generate_research_report()")
        pdf_path = generate_research_report(
            topic="Artificial Intelligence",
            papers=test_papers,
            emerging_trends=test_trends,
            filename="test_research_report.pdf"
        )
        assert Path(pdf_path).exists()
        file_size = Path(pdf_path).stat().st_size
        assert file_size > 1000, f"PDF too small: {file_size} bytes"
        print("✓")
        
        print_test("generate_detailed_analysis_report()")
        pdf_path = generate_detailed_analysis_report(
            topic="Artificial Intelligence",
            papers=test_papers,
            emerging_trends=test_trends,
            filename="test_detailed_analysis.pdf"
        )
        assert Path(pdf_path).exists()
        file_size = Path(pdf_path).stat().st_size
        assert file_size > 2000, f"PDF too small: {file_size} bytes"
        print("✓")
        
        print("\n  ✅ PDF Generator tests passed!\n")
        return True
    
    except Exception as e:
        print(f"✗\n  ❌ PDF Generator test failed: {str(e)}\n")
        return False


def test_main_orchestrator() -> bool:
    """Test main orchestrator with mock data."""
    print_section("TEST 4: Main Orchestrator")
    
    try:
        print_test("ResearchAnalyzer initialization")
        analyzer = ResearchAnalyzer()
        assert analyzer is not None
        print("✓")
        
        print_test("get_analysis_summary() with mock data")
        mock_result = {
            "status": "success",
            "message": "Test message",
            "papers": [
                {"title": "P1", "topics": ["AI"]},
                {"title": "P2", "topics": ["ML"]},
            ],
            "trends": {
                "trends": ["Agentic AI", "Tool Calling"],
                "total_trends": 2,
                "analysis": "Test analysis"
            },
            "statistics": {
                "total_papers": 2,
                "unique_topics": 2,
                "avg_topics_per_paper": 1.0,
                "most_common_topics": [
                    {"topic": "AI", "count": 1},
                    {"topic": "ML", "count": 1}
                ]
            },
            "pdf_path": None
        }
        summary = analyzer.get_analysis_summary(mock_result)
        assert "Analysis Summary" in summary
        assert "Papers Analyzed: 2" in summary
        print("✓")
        
        print("\n  ✅ Main Orchestrator tests passed!\n")
        return True
    
    except Exception as e:
        print(f"✗\n  ❌ Main Orchestrator test failed: {str(e)}\n")
        return False


def test_directory_structure() -> bool:
    """Test project directory structure."""
    print_section("TEST 5: Directory Structure")
    
    try:
        print_test("agents/ directory")
        agents_dir = Path("agents")
        assert agents_dir.exists()
        assert (agents_dir / "search_agent.py").exists()
        assert (agents_dir / "summary_agent.py").exists()
        assert (agents_dir / "topic_agent.py").exists()
        assert (agents_dir / "trend_agent.py").exists()
        print("✓")
        
        print_test("tools/ directory")
        tools_dir = Path("tools")
        assert tools_dir.exists()
        assert (tools_dir / "paper_counter.py").exists()
        assert (tools_dir / "pdf_generator.py").exists()
        print("✓")
        
        print_test("app/ directory")
        app_dir = Path("app")
        assert app_dir.exists()
        assert (app_dir / "streamlit_app.py").exists()
        print("✓")
        
        print_test("config.py and main.py")
        assert Path("config.py").exists()
        assert Path("main.py").exists()
        print("✓")
        
        print_test("outputs/ directory creation")
        outputs_dir = Path("outputs")
        assert outputs_dir.exists()
        assert (outputs_dir / "reports").exists()
        assert (outputs_dir / "logs").exists()
        print("✓")
        
        print("\n  ✅ Directory structure tests passed!\n")
        return True
    
    except Exception as e:
        print(f"✗\n  ❌ Directory structure test failed: {str(e)}\n")
        return False


def test_imports() -> bool:
    """Test that all modules can be imported."""
    print_section("TEST 6: Import Checks")
    
    try:
        print_test("config module")
        from config import Config, logger
        print("✓")
        
        print_test("tools.paper_counter")
        from tools.paper_counter import calculate_paper_statistics
        print("✓")
        
        print_test("tools.pdf_generator")
        from tools.pdf_generator import generate_research_report
        print("✓")
        
        print_test("agents.search_agent")
        from agents.search_agent import search_papers, initialize_gemini
        print("✓")
        
        print_test("agents.summary_agent")
        from agents.summary_agent import summarize_papers
        print("✓")
        
        print_test("agents.topic_agent")
        from agents.topic_agent import extract_topics_from_papers
        print("✓")
        
        print_test("agents.trend_agent")
        from agents.trend_agent import identify_trends
        print("✓")
        
        print_test("main module")
        from main import ResearchAnalyzer
        print("✓")
        
        print("\n  ✅ Import checks passed!\n")
        return True
    
    except Exception as e:
        print(f"✗\n  ❌ Import check failed: {str(e)}\n")
        return False


def run_all_tests() -> Dict[str, bool]:
    """Run all tests and return results."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "ResearchMind AI - Test Suite" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")
    
    results = {
        "Configuration": test_config(),
        "Paper Counter": test_paper_counter(),
        "PDF Generator": test_pdf_generator(),
        "Main Orchestrator": test_main_orchestrator(),
        "Directory Structure": test_directory_structure(),
        "Import Checks": test_imports(),
    }
    
    return results


def print_test_summary(results: Dict[str, bool]) -> None:
    """Print test results summary."""
    print_section("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = "✅ PASS" if passed_flag else "❌ FAIL"
        print(f"  {status:8} | {test_name}")
    
    print(f"\n  {'-' * 50}")
    print(f"  Result: {passed}/{total} tests passed")
    print(f"  {'-' * 50}\n")
    
    if passed == total:
        print("  🎉 All tests passed! System is ready for use.\n")
        return True
    else:
        print(f"  ⚠️  {total - passed} test(s) failed. Please review errors above.\n")
        return False


if __name__ == "__main__":
    try:
        results = run_all_tests()
        success = print_test_summary(results)
        
        if success:
            print("  Next steps:")
            print("  1. Test with Streamlit: streamlit run app/streamlit_app.py")
            print("  2. Test CLI: python main.py")
            print("  3. Review generated PDFs in outputs/reports/\n")
        
        sys.exit(0 if success else 1)
    
    except Exception as e:
        print(f"\n❌ Fatal error during testing: {str(e)}\n")
        sys.exit(1)
