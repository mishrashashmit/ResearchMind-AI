"""Main orchestrator for ResearchMind AI.

Combines all agents and tools into a unified research analysis pipeline.
Provides both programmatic and CLI interfaces for paper research and analysis.
"""

from typing import Any, Dict, List

from agents.search_agent import search_papers
from agents.summary_agent import summarize_papers
from agents.topic_agent import extract_topics_from_papers, get_all_topics
from agents.trend_agent import identify_trends, analyze_trend_frequency, get_trend_report
from tools.paper_counter import (
    calculate_paper_statistics,
    count_papers_by_topic,
    get_trending_topics,
)
from tools.pdf_generator import (
    generate_research_report,
    generate_detailed_analysis_report,
)
from config import Config, logger


class ResearchAnalyzer:
    """Orchestrator class for complete research analysis pipeline.
    
    Coordinates all agents (search, summary, topic, trend) to perform
    comprehensive research paper analysis.
    """
    
    def __init__(self) -> None:
        """Initialize the ResearchAnalyzer."""
        logger.info("ResearchAnalyzer initialized")
    
    def analyze_research_topic(
        self,
        topic: str,
        num_papers: int = 5,
        generate_pdf: bool = False,
        report_type: str = "summary"
    ) -> Dict[str, Any]:
        """Execute complete research analysis pipeline for a given topic.
        
        Performs the following steps:
        1. Search for research papers on the topic
        2. Generate detailed summaries for each paper
        3. Extract key topics from papers
        4. Identify emerging research trends
        5. Calculate statistics
        6. Optionally generate PDF report
        
        Args:
            topic: Research topic to analyze (e.g., "artificial intelligence").
            num_papers: Number of papers to search for (default: 5, max: 10).
            generate_pdf: Whether to generate a PDF report (default: False).
            report_type: Type of report ("summary" or "detailed").
        
        Returns:
            Dictionary containing:
            - papers: List of analyzed papers with summaries and topics
            - trends: Identified research trends
            - statistics: Paper and topic statistics
            - pdf_path: Path to generated PDF (if requested)
            - status: "success" or "error"
            - message: Status message
        
        Raises:
            ValueError: If topic is empty or invalid.
            Exception: If analysis pipeline fails.
        
        Example:
            >>> analyzer = ResearchAnalyzer()
            >>> result = analyzer.analyze_research_topic(
            ...     "machine learning",
            ...     num_papers=5,
            ...     generate_pdf=True,
            ...     report_type="summary"
            ... )
            >>> print(result['status'])
            'success'
        """
        if not isinstance(topic, str) or not topic.strip():
            logger.error("Invalid topic provided to analyze_research_topic")
            raise ValueError("Topic must be a non-empty string")
        
        result: Dict[str, Any] = {
            "status": "error",
            "message": "",
            "papers": [],
            "trends": {},
            "statistics": {},
            "pdf_path": None,
        }
        
        try:
            logger.info(f"Starting analysis for topic: {topic}")
            
            logger.info("Step 1: Searching for papers...")
            papers = search_papers(topic, num_papers=num_papers)
            if not papers:
                result["message"] = "No papers found for the given topic."
                logger.warning(f"No papers found for topic: {topic}")
                return result
            
            logger.info(f"Step 2: Found {len(papers)} papers, generating summaries...")
            summarized_papers = summarize_papers(papers)
            
            logger.info("Step 3: Extracting topics from papers...")
            papers_with_topics = extract_topics_from_papers(summarized_papers)
            
            logger.info("Step 4: Identifying research trends...")
            trends_result = identify_trends(papers_with_topics)
            
            logger.info("Step 5: Calculating statistics...")
            statistics = calculate_paper_statistics(papers_with_topics)
            
            result["papers"] = papers_with_topics
            result["trends"] = trends_result
            result["statistics"] = statistics
            
            if generate_pdf:
                logger.info(f"Step 6: Generating {report_type} PDF report...")
                if report_type.lower() == "detailed":
                    pdf_path = generate_detailed_analysis_report(
                        topic=topic,
                        papers=papers_with_topics,
                        emerging_trends=trends_result.get("trends", []),
                        filename=f"detailed_analysis_{topic.replace(' ', '_')}.pdf"
                    )
                else:
                    pdf_path = generate_research_report(
                        topic=topic,
                        papers=papers_with_topics,
                        emerging_trends=trends_result.get("trends", []),
                        filename=f"research_report_{topic.replace(' ', '_')}.pdf"
                    )
                result["pdf_path"] = pdf_path
                logger.info(f"PDF report generated: {pdf_path}")
            
            result["status"] = "success"
            result["message"] = (
                f"Analysis completed: {len(papers_with_topics)} papers analyzed, "
                f"{trends_result['total_trends']} trends identified."
            )
            logger.info(f"Analysis completed successfully for topic: {topic}")
            
            return result
        
        except Exception as e:
            result["message"] = f"Analysis failed: {str(e)}"
            logger.error(f"Error during analysis: {str(e)}")
            return result
    
    def get_analysis_summary(
        self,
        analysis_result: Dict[str, Any]
    ) -> str:
        """Generate a human-readable summary of analysis results.
        
        Args:
            analysis_result: Dictionary returned by analyze_research_topic().
        
        Returns:
            str: Formatted summary text.
        """
        if analysis_result["status"] != "success":
            return f"Analysis failed: {analysis_result['message']}"
        
        papers_count = len(analysis_result["papers"])
        trends = analysis_result["trends"].get("trends", [])
        stats = analysis_result["statistics"]
        
        summary = f"""
        
               ResearchMind AI - Analysis Summary


📊 Papers Analyzed: {papers_count}
📈 Trends Identified: {len(trends)}
🏷️  Unique Topics: {stats.get('unique_topics', 0)}
📐 Avg Topics/Paper: {stats.get('avg_topics_per_paper', 0)}

🔍 Top Research Trends:
{chr(10).join([f'   • {trend}' for trend in trends[:5]])}

🏆 Most Common Topics:
{chr(10).join([f"   • {t['topic']} ({t['count']} papers)" for t in stats.get('most_common_topics', [])[:5]])}

{'✓ PDF Report: Generated' if analysis_result['pdf_path'] else ''}
"""
        return summary


def run_cli() -> None:
    """Run interactive CLI for ResearchMind AI."""
    print("\n" + "=" * 60)
    print("ResearchMind AI - Multi-Agent Research Assistant")
    print("=" * 60)
    
    analyzer = ResearchAnalyzer()
    
    while True:
        print("\n🔬 ResearchMind CLI")
        print("-" * 60)
        print("1. Analyze research topic")
        print("2. Exit")
        print("-" * 60)
        
        choice = input("Select option (1-2): ").strip()
        
        if choice == "1":
            topic = input("\n📝 Enter research topic: ").strip()
            
            if not topic:
                print("⚠️  Topic cannot be empty.")
                continue
            
            num_papers_input = input("📊 Number of papers (1-10, default 5): ").strip()
            try:
                num_papers = int(num_papers_input) if num_papers_input else 5
                num_papers = max(1, min(num_papers, 10))
            except ValueError:
                num_papers = 5
            
            generate_pdf_input = input("📄 Generate PDF report? (y/n, default n): ").strip().lower()
            generate_pdf = generate_pdf_input in ("y", "yes")
            
            report_type = "summary"
            if generate_pdf:
                report_type_input = input("📋 Report type (summary/detailed, default summary): ").strip().lower()
                report_type = "detailed" if report_type_input == "detailed" else "summary"
            
            print("\n⏳ Analyzing research papers...")
            print("-" * 60)
            
            result = analyzer.analyze_research_topic(
                topic=topic,
                num_papers=num_papers,
                generate_pdf=generate_pdf,
                report_type=report_type
            )
            
            print(analyzer.get_analysis_summary(result))
            
            if result["status"] == "success":
                print("\n📄 Papers Found:")
                for idx, paper in enumerate(result["papers"], 1):
                    print(f"\n   {idx}. {paper.get('title', 'Untitled')}")
                    print(f"      Year: {paper.get('year', 'N/A')}")
                    print(f"      Topics: {', '.join(paper.get('topics', []))}")
                
                if result["pdf_path"]:
                    print(f"\n✓ PDF saved to: {result['pdf_path']}")
            else:
                print(f"\n Error: {result['message']}")
        
        elif choice == "2":
            print("\n👋 Thank you for using ResearchMind AI!")
            break
        
        else:
            print(" Invalid option. Please select 1 or 2.")


def main() -> None:
    """Main entry point for ResearchMind AI.
    
    Can be used as:
    - CLI: python main.py
    - Programmatic: from main import ResearchAnalyzer
    """
    try:
        Config.validate_config()
        run_cli()
    except ValueError as e:
        print(f" Configuration error: {str(e)}")
        print("Please set GEMINI_API_KEY in .env file.")
    except Exception as e:
        logger.error(f"Fatal error in main: {str(e)}")
        print(f" Fatal error: {str(e)}")


if __name__ == "__main__":
    main()
