"""Paper statistics and counting utilities for ResearchMind AI.

Provides functions to count papers, calculate statistics,
and analyze paper distributions.
"""

from typing import Any, Dict, List


def count_papers(papers: List[Dict[str, Any]]) -> int:
    """Count the total number of papers in a list.
    
    Args:
        papers: List of paper dictionaries.
    
    Returns:
        int: Total count of papers.
    
    Example:
        >>> papers = [{"title": "Paper 1"}, {"title": "Paper 2"}]
        >>> count_papers(papers)
        2
    """
    if not isinstance(papers, list):
        return 0
    return len(papers)


def count_papers_by_topic(papers: List[Dict[str, Any]]) -> Dict[str, int]:
    """Count papers grouped by topic.
    
    Args:
        papers: List of paper dictionaries with "topics" key.
    
    Returns:
        Dict mapping topic names to paper counts.
    
    Example:
        >>> papers = [
        ...     {"title": "P1", "topics": ["AI", "ML"]},
        ...     {"title": "P2", "topics": ["AI", "NLP"]}
        ... ]
        >>> count_papers_by_topic(papers)
        {'AI': 2, 'ML': 1, 'NLP': 1}
    """
    topic_counts: Dict[str, int] = {}
    
    if not isinstance(papers, list):
        return topic_counts
    
    for paper in papers:
        if not isinstance(paper, dict):
            continue
        
        topics = paper.get("topics", [])
        if not isinstance(topics, list):
            continue
        
        for topic in topics:
            if isinstance(topic, str):
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
    
    return topic_counts


def calculate_paper_statistics(papers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate comprehensive statistics for a collection of papers.
    
    Args:
        papers: List of paper dictionaries.
    
    Returns:
        Dictionary with statistics:
        - total_papers: Total paper count
        - unique_topics: Count of unique topics
        - avg_topics_per_paper: Average topics per paper
        - most_common_topics: Top 5 most frequent topics
        - summary_length_stats: Stats about summary lengths
    
    Example:
        >>> papers = [{"title": "P1", "topics": ["AI"]}, {"title": "P2", "topics": ["ML"]}]
        >>> stats = calculate_paper_statistics(papers)
        >>> stats["total_papers"]
        2
    """
    stats: Dict[str, Any] = {
        "total_papers": 0,
        "unique_topics": 0,
        "avg_topics_per_paper": 0.0,
        "most_common_topics": [],
        "summary_length_stats": {
            "min_length": 0,
            "max_length": 0,
            "avg_length": 0.0
        }
    }
    
    if not isinstance(papers, list) or len(papers) == 0:
        return stats
    
    stats["total_papers"] = len(papers)
    
    topic_counts = count_papers_by_topic(papers)
    stats["unique_topics"] = len(topic_counts)
    
    total_topics = sum(topic_counts.values())
    stats["avg_topics_per_paper"] = round(total_topics / len(papers), 2)
    
    sorted_topics = sorted(
        topic_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )
    stats["most_common_topics"] = [
        {"topic": topic, "count": count}
        for topic, count in sorted_topics[:5]
    ]
    
    summary_lengths: List[int] = []
    for paper in papers:
        if isinstance(paper, dict):
            summary = paper.get("summary", "")
            if isinstance(summary, str):
                summary_lengths.append(len(summary))
    
    if summary_lengths:
        stats["summary_length_stats"]["min_length"] = min(summary_lengths)
        stats["summary_length_stats"]["max_length"] = max(summary_lengths)
        stats["summary_length_stats"]["avg_length"] = round(
            sum(summary_lengths) / len(summary_lengths),
            2
        )
    
    return stats


def filter_papers_by_topic(
    papers: List[Dict[str, Any]],
    topic: str
) -> List[Dict[str, Any]]:
    """Filter papers that contain a specific topic.
    
    Args:
        papers: List of paper dictionaries with "topics" key.
        topic: Topic to filter by.
    
    Returns:
        List of papers containing the specified topic.
    
    Example:
        >>> papers = [
        ...     {"title": "P1", "topics": ["AI"]},
        ...     {"title": "P2", "topics": ["ML"]}
        ... ]
        >>> filter_papers_by_topic(papers, "AI")
        [{"title": "P1", "topics": ["AI"]}]
    """
    if not isinstance(papers, list) or not isinstance(topic, str):
        return []
    
    filtered = []
    for paper in papers:
        if not isinstance(paper, dict):
            continue
        
        topics = paper.get("topics", [])
        if isinstance(topics, list) and topic in topics:
            filtered.append(paper)
    
    return filtered


def get_trending_topics(
    papers: List[Dict[str, Any]],
    min_occurrences: int = 2
) -> List[Dict[str, Any]]:
    """Get trending topics based on minimum occurrence threshold.
    
    Args:
        papers: List of paper dictionaries with "topics" key.
        min_occurrences: Minimum times a topic must appear to be considered trending.
    
    Returns:
        List of trending topics sorted by frequency (highest first).
    
    Example:
        >>> papers = [
        ...     {"topics": ["AI", "ML"]},
        ...     {"topics": ["AI", "NLP"]},
        ...     {"topics": ["CV"]}
        ... ]
        >>> get_trending_topics(papers, min_occurrences=2)
        [{"topic": "AI", "count": 2}]
    """
    if not isinstance(papers, list) or not isinstance(min_occurrences, int):
        return []
    
    topic_counts = count_papers_by_topic(papers)
    
    trending = [
        {"topic": topic, "count": count}
        for topic, count in sorted(
            topic_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        if count >= min_occurrences
    ]
    
    return trending
