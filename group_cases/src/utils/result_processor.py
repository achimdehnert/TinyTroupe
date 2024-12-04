"""
Utility module for processing and formatting discussion results.
"""
from typing import Dict, List, Any
import json
from collections import defaultdict

def format_results(raw_results: List[Dict[str, Any]], discussion_type: str) -> Dict[str, Any]:
    """
    Format raw discussion results based on discussion type.
    
    Args:
        raw_results: List of raw results from discussion steps
        discussion_type: Type of discussion
        
    Returns:
        Formatted results
    """
    if discussion_type == "brainstorming":
        return format_brainstorming_results(raw_results)
    elif discussion_type == "evaluation":
        return format_evaluation_results(raw_results)
    elif discussion_type == "interview":
        return format_interview_results(raw_results)
    else:
        return format_generic_results(raw_results)

def format_brainstorming_results(raw_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Format brainstorming results with ideas, themes, and priorities."""
    ideas = []
    themes = defaultdict(list)
    priorities = defaultdict(int)
    
    for step in raw_results:
        for response in step["responses"]:
            # Extract ideas from responses
            if "ideas" in response:
                ideas.extend(response["ideas"])
                
            # Group ideas into themes
            if "theme" in response:
                themes[response["theme"]].append(response["content"])
                
            # Track idea priorities
            if "priority" in response:
                priorities[response["content"]] = response["priority"]
    
    return {
        "ideas": ideas,
        "themes": dict(themes),
        "priorities": dict(priorities),
        "summary": _extract_summary(raw_results)
    }

def format_evaluation_results(raw_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Format evaluation results with scores, insights, and recommendations."""
    scores = defaultdict(list)
    insights = []
    recommendations = []
    
    for step in raw_results:
        for response in step["responses"]:
            # Collect scores
            if "scores" in response:
                for criterion, score in response["scores"].items():
                    scores[criterion].append(score)
            
            # Gather insights and recommendations
            if "insights" in response:
                insights.extend(response["insights"])
            if "recommendations" in response:
                recommendations.extend(response["recommendations"])
    
    # Calculate average scores
    avg_scores = {
        criterion: sum(scores)/len(scores) 
        for criterion, scores in scores.items()
    }
    
    return {
        "scores": avg_scores,
        "insights": insights,
        "recommendations": recommendations,
        "summary": _extract_summary(raw_results)
    }

def format_interview_results(raw_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Format interview results with key findings and quotes."""
    key_findings = []
    quotes = []
    themes = defaultdict(list)
    
    for step in raw_results:
        for response in step["responses"]:
            # Extract key findings
            if "findings" in response:
                key_findings.extend(response["findings"])
            
            # Collect notable quotes
            if "quotes" in response:
                quotes.extend(response["quotes"])
            
            # Group by themes
            if "theme" in response:
                themes[response["theme"]].append(response["content"])
    
    return {
        "key_findings": key_findings,
        "quotes": quotes,
        "themes": dict(themes),
        "summary": _extract_summary(raw_results)
    }

def format_generic_results(raw_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Format generic discussion results."""
    key_points = []
    consensus_items = []
    action_items = []
    
    for step in raw_results:
        # Extract key points from step summary
        if "summary" in step:
            if "key_points" in step["summary"]:
                key_points.extend(step["summary"]["key_points"])
            if "consensus" in step["summary"]:
                consensus_items.append(step["summary"]["consensus"])
            if "action_items" in step["summary"]:
                action_items.extend(step["summary"]["action_items"])
    
    return {
        "key_points": key_points,
        "consensus": consensus_items,
        "action_items": action_items,
        "summary": _extract_summary(raw_results)
    }

def _extract_summary(raw_results: List[Dict[str, Any]]) -> str:
    """Extract overall summary from results."""
    summaries = []
    for step in raw_results:
        if "summary" in step:
            summaries.append(step["summary"])
    
    # Combine summaries into overall summary
    # TODO: Implement with more sophisticated text summarization
    return " ".join(str(s) for s in summaries)
