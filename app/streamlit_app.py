"""Streamlit web application for ResearchMind AI.

Interactive interface for research paper analysis with topic extraction,
trend identification, and PDF report generation.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from agents.search_agent import search_papers
from agents.summary_agent import summarize_papers
from agents.topic_agent import extract_topics_from_papers, get_all_topics
from agents.trend_agent import identify_trends, analyze_trend_frequency
from tools.paper_counter import calculate_paper_statistics, get_trending_topics
from tools.pdf_generator import generate_research_report

from config import logger

st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Global font */
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', 'Inter', 'Roboto', sans-serif;
    }

    /* Main title */
    h1 {
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* Subheaders */
    h2, h3 {
        font-weight: 600;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        font-size: 14px;
    }

    /* Buttons */
    button {
        border-radius: 8px !important;
        font-weight: 500 !important;
    }

    /* Expander text */
    .streamlit-expanderHeader {
        font-weight: 500;
    }

    /* Reduce clutter spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
/* Cards feel */
div.stDataFrame, div.stExpander {
    border-radius: 12px;
}

/* Metric boxes */
[data-testid="stMetric"] {
    background-color: #111827;
    padding: 12px;
    border-radius: 10px;
    color: white;
}

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}
</style>
""", unsafe_allow_html=True)


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "search_results" not in st.session_state:
        st.session_state.search_results = None
    if "summaries" not in st.session_state:
        st.session_state.summaries = None
    if "topics_extracted" not in st.session_state:
        st.session_state.topics_extracted = None
    if "trends" not in st.session_state:
        st.session_state.trends = None
    if "current_topic" not in st.session_state:
        st.session_state.current_topic = ""
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    if "topic_history" not in st.session_state:
        st.session_state.topic_history = []


def display_header() -> None:
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 40px;
            font-weight: 800;
            text-align: center;
            background: linear-gradient(90deg, #4F46E5, #06B6D4, #10B981);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }

        .sub-header {
            text-align: center;
            font-size: 16px;
            color: #6B7280;
            margin-bottom: 20px;
        }
        </style>

        <div class="main-header">ResearchMind AI</div>
        <div class="sub-header">Your Research Companion</div>
        """,
        unsafe_allow_html=True
    )


def display_sidebar() -> None:
    """Display sidebar with app info and settings."""
    with st.sidebar:

        #ABOUT
        with st.expander("About ResearchMind AI", expanded=True):
            st.info(
                "ResearchMind AI analyzes research papers using AI-powered agents to help you:\n\n"
                "\n• Search for relevant papers\n"
                "\n• Generate detailed summaries\n"
                "\n• Extract key topics\n"
                "\n• Identify emerging trends\n"
                "\n• Generate PDF reports"
            )

        #SETTINGS
        with st.expander("Settings", expanded=True):

            num_papers = st.slider(
                "Number of papers to search",
                min_value=1,
                max_value=10,
                value=5
            )
            st.session_state.num_papers = num_papers

            report_type = st.radio(
                "Report type",
                options=["Summary", "Detailed"]
            )
            st.session_state.report_type = report_type

        #STATUS
        with st.expander("System Status", expanded=False):
            st.success("Backend: Active")
            st.info("Gemini API: Connected (when quota available)")
            st.write("Pipeline: Search → Summarize → Topics → Trends")

        #FOOTER
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; font-size: 11px; color: gray;'>
                Developed by <b>AI & Software Enthusiasts</b><br>
                Shashmit Mishra & Sanskar Pandey
            </div>
            """,
            unsafe_allow_html=True
        )


def display_search_section() -> None:
    """Display research topic search section."""
    st.markdown("### Research Topic")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        topic = st.text_input(
            "Enter research topic",
            placeholder="e.g., artificial intelligence, machine learning, quantum computing",
            label_visibility="collapsed"
        )
    
    with col2:
        analyze_button = st.button("Analyze", use_container_width=True)
    
    return topic, analyze_button


def run_analysis(topic: str, num_papers: int) -> bool:
    """Execute full research analysis pipeline."""
    try:
        #SEARCH
        with st.spinner("Searching for papers..."):
            papers = search_papers(topic, num_papers=num_papers)

            if not papers:
                st.error("No papers found for the given topic.")
                return False

            st.session_state.search_results = papers
            logger.info(f"Found {len(papers)} papers")

        #SUMMARY
        with st.spinner("Generating summaries..."):
            summarized = summarize_papers(papers)
            st.session_state.summaries = summarized
            logger.info(f"Generated {len(summarized)} summaries")

        #TOPICS
        with st.spinner("Extracting topics..."):
            try:
                topics_data = extract_topics_from_papers(summarized)

                if not topics_data:
                    st.warning(
                        "Topics could not be extracted from papers, "
                        "but summaries and search results are still available."
                    )
                    topics_data = []

                st.session_state.topics_extracted = topics_data
                logger.info(f"Extracted topics from {len(topics_data)} papers")

            except Exception as e:
                logger.warning(f"Topic extraction failed gracefully: {e}")
                st.session_state.topics_extracted = []
                topics_data = []

        #TRENDS
        with st.spinner("Identifying trends..."):
            try:
                if len(summarized) < 2:
                    trends_result = {
                        "trends": [],
                        "total_trends": 0,
                        "analysis": (
                            "Not enough papers to identify trends "
                            "(minimum 2 required)."
                        )
                    }
                else:
                    trends_result = identify_trends(topics_data)

                st.session_state.trends = trends_result
                logger.info(f"Trends processed: {trends_result['total_trends']}")

            except Exception as e:
                logger.warning(f"Trend analysis failed: {e}")
                st.session_state.trends = {
                    "trends": [],
                    "total_trends": 0,
                    "analysis": "Trend analysis failed safely."
                }

        #FINAL STATE
        st.session_state.analysis_complete = True
        st.session_state.current_topic = topic

        if topic not in st.session_state.topic_history:
            st.session_state.topic_history.append(topic)

        logger.info("Analysis pipeline completed successfully")
        return True

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        st.error(f"Analysis failed: {str(e)}")
        return False


def display_statistics() -> None:
    """Display paper statistics and overview."""
    if not st.session_state.search_results:
        return
    
    papers = st.session_state.search_results
    
    st.markdown("### Analysis Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Papers Found",
            value=len(papers),
            help="Total number of research papers analyzed"
        )
    
    if st.session_state.topics_extracted:
        unique_topics_set = set()
        for paper in st.session_state.topics_extracted:
            topics = paper.get("topics", [])
            if isinstance(topics, list):
                unique_topics_set.update(topics)
        
        with col2:
            st.metric(
                label="Unique Topics",
                value=len(unique_topics_set),
                help="Number of unique topics identified"
            )
    
    if st.session_state.trends:
        with col3:
            st.metric(
                label="Research Trends",
                value=st.session_state.trends["total_trends"],
                help="Number of emerging research trends"
            )
    
    with col4:
        st.metric(
            label="Analysis Status",
            value="✓ Done" if st.session_state.analysis_complete else "○ Pending",
            help="Current analysis status"
        )


def display_papers_section() -> None:
    """Display papers with summaries."""
    if not st.session_state.summaries:
        return
    
    st.markdown("### Research Papers")
    
    papers = st.session_state.summaries
    
    for idx, paper in enumerate(papers, 1):
        with st.expander(
            f"Paper {idx}: {paper.get('title', 'Untitled')[:60]}",
            expanded=False
        ):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Title:** {paper.get('title', 'N/A')}")
                st.markdown(f"**Year:** {paper.get('year', 'N/A')}")
            
            with col2:
                st.markdown(f"**Status:** ✓ Analyzed")
            
            st.markdown("**Brief Summary:**")
            st.write(paper.get("summary", "No summary available"))
            
            if paper.get("detailed_summary"):
                st.markdown("**Detailed Summary:**")
                st.write(paper["detailed_summary"])


def display_topics_section() -> None:
    """Display extracted topics."""
    if not st.session_state.topics_extracted:
        return
    
    st.markdown("### Here Are The Extracted Topics")
    
    all_topics_result = get_all_topics(st.session_state.topics_extracted)
    all_topics = all_topics_result.get("topics", [])
    
    if all_topics:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info(f"**Total unique topics:** {len(all_topics)}")
        
        with col2:
            st.success(f"**Coverage:** {len(st.session_state.topics_extracted)} papers")
        
        cols = st.columns(3)
        for idx, topic in enumerate(all_topics[:12]):
            with cols[idx % 3]:
                st.markdown(f"• {topic}")
        
        if len(all_topics) > 12:
            with st.expander(f"Show all {len(all_topics)} topics"):
                for topic in all_topics:
                    st.write(f"• {topic}")
    else:
        st.info("No topics identified yet.")


def display_trends_section() -> None:
    """Display identified research trends."""
    if not st.session_state.trends:
        return
    
    st.markdown("### Here Are The Research Trends")
    
    trends = st.session_state.trends.get("trends", [])
    
    if trends:
        st.markdown(f"**{len(trends)} Emerging Trends Identified:**")
        
        for idx, trend in enumerate(trends, 1):
            st.markdown(f"**{idx}. {trend}**")
        
        if st.session_state.trends.get("analysis"):
            st.markdown("**Trend Analysis:**")
            st.info(st.session_state.trends["analysis"])
    else:
        st.info("No trends identified yet.")


def display_download_section() -> None:
    if not st.session_state.analysis_complete:
        return

    st.markdown("### Download Report")

    try:
        topic = st.session_state.current_topic
        trends = st.session_state.trends.get("trends", [])

        if st.button("Generate PDF Report", use_container_width=True):
            with st.spinner("Generating PDF..."):

                # FIX: BUILD ENRICHED PAPERS

                enriched_papers = []

                summaries = st.session_state.summaries or []
                topics_data = st.session_state.topics_extracted or []

                for i, p in enumerate(summaries):
                    topics = []

                    if i < len(topics_data):
                        topics = topics_data[i].get("topics", [])

                    enriched_papers.append({
                        "title": p.get("title", ""),
                        "summary": p.get("summary", ""),
                        "year": p.get("year", ""),
                        "topics": topics
                    })

                # PDF GENERATION
                pdf_path = generate_research_report(
                    topic=topic,
                    papers=enriched_papers, 
                    emerging_trends=trends,
                    filename=f"research_{topic.replace(' ', '_')}.pdf"
                )

                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF",
                        data=pdf_file.read(),
                        file_name=Path(pdf_path).name,
                        mime="application/pdf",
                    )

                st.success("PDF generated successfully")

    except Exception as e:
        st.error(f"Error generating report: {str(e)}")


def main() -> None:
    """Main application entry point."""
    initialize_session_state()

    display_header()

    
    # LAYOUT: LEFT + RIGHT
    
    col_main, col_right = st.columns([3, 1])

    # LEFT SIDE (APP)
   
    with col_main:
        display_sidebar()

        st.markdown("---")

        topic, analyze_button = display_search_section()

        if analyze_button:
            if not topic.strip():
                st.warning("Please enter a research topic.")
            else:
                num_papers = getattr(st.session_state, "num_papers", 5)

                if run_analysis(topic, num_papers):
                    st.session_state.current_topic = topic

                    # store history (avoid duplicates)
                    if topic not in st.session_state.topic_history:
                        st.session_state.topic_history.append(topic)

                    st.success("Analysis completed successfully!")

        st.markdown("---")

        if st.session_state.analysis_complete:
            display_statistics()

            st.markdown("---")

            display_papers_section()
            display_topics_section()
            display_trends_section()

            st.markdown("---")

            display_download_section()

    # RIGHT SIDE (HISTORY PANEL)
    with col_right:
        st.markdown("### Search History")

        with st.expander("History Panel", expanded=True):

            if st.session_state.topic_history:

                # Clear history with confirmation
                if st.button("Clear History"):
                    st.session_state._confirm_clear = True

                if st.session_state.get("_confirm_clear", False):
                    st.warning("Are you sure you want to clear history?")

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("Yes, Clear"):
                            st.session_state.topic_history = []
                            st.session_state._confirm_clear = False
                            st.rerun()

                    with col2:
                        if st.button("Cancel"):
                            st.session_state._confirm_clear = False
                            st.rerun()

                st.markdown("---")

                # show history
                for i, t in enumerate(
                    reversed(st.session_state.topic_history[-10:]), 1
                ):
                    st.markdown(f"{i}. {t}")

            else:
                st.info("No search history yet")
    # FOOTER
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #888;">
        <small>ResearchMind AI | Powered by Gemini API</small>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()