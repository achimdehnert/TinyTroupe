"""
Advanced analytics module for discussion analysis.
"""
from typing import Dict, List, Any, Optional
import numpy as np
from collections import defaultdict
from datetime import datetime, timedelta
from ..tools.word_processor import WordProcessor

class DiscussionAnalytics:
    """Advanced analytics for discussion analysis."""
    
    def __init__(self):
        """Initialize analytics engine."""
        self.word_processor = WordProcessor()
        
    def analyze_discussion_dynamics(
        self,
        messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze discussion dynamics and patterns.
        
        Args:
            messages: List of discussion messages
            
        Returns:
            Analysis results
        """
        return {
            "participation_metrics": self._analyze_participation(messages),
            "interaction_patterns": self._analyze_interactions(messages),
            "topic_evolution": self._analyze_topic_evolution(messages),
            "engagement_metrics": self._analyze_engagement(messages),
            "discussion_flow": self._analyze_discussion_flow(messages)
        }
        
    def _analyze_participation(
        self,
        messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze participation patterns."""
        participant_stats = defaultdict(lambda: {
            "message_count": 0,
            "total_words": 0,
            "avg_message_length": 0,
            "response_times": [],
            "active_periods": []
        })
        
        last_message_time = None
        for msg in messages:
            sender = msg["sender"]
            timestamp = datetime.fromisoformat(msg["timestamp"])
            content = msg["content"]
            
            # Update basic stats
            participant_stats[sender]["message_count"] += 1
            words = len(content.split())
            participant_stats[sender]["total_words"] += words
            
            # Track response times
            if last_message_time:
                response_time = (timestamp - last_message_time).total_seconds()
                participant_stats[sender]["response_times"].append(response_time)
            last_message_time = timestamp
            
            # Track active periods
            participant_stats[sender]["active_periods"].append(timestamp)
            
        # Calculate averages and activity patterns
        for participant in participant_stats.values():
            if participant["message_count"] > 0:
                participant["avg_message_length"] = (
                    participant["total_words"] / participant["message_count"]
                )
            if participant["response_times"]:
                participant["avg_response_time"] = (
                    sum(participant["response_times"]) /
                    len(participant["response_times"])
                )
            
            # Calculate activity patterns
            times = participant["active_periods"]
            if times:
                participant["activity_duration"] = (
                    (max(times) - min(times)).total_seconds() / 3600
                )  # in hours
                
        return dict(participant_stats)
        
    def _analyze_interactions(
        self,
        messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze interaction patterns between participants."""
        interaction_matrix = defaultdict(lambda: defaultdict(int))
        reference_patterns = defaultdict(list)
        
        for i, msg in enumerate(messages):
            sender = msg["sender"]
            content = msg["content"].lower()
            
            # Look for direct mentions or references
            for prev_msg in messages[max(0, i-5):i]:
                prev_sender = prev_msg["sender"]
                if prev_sender != sender and (
                    prev_sender.lower() in content or
                    self._has_reference(content, prev_msg["content"])
                ):
                    interaction_matrix[sender][prev_sender] += 1
                    reference_patterns[sender].append({
                        "referenced": prev_sender,
                        "context": content,
                        "timestamp": msg["timestamp"]
                    })
                    
        return {
            "interaction_matrix": dict(interaction_matrix),
            "reference_patterns": dict(reference_patterns)
        }
        
    def _analyze_topic_evolution(
        self,
        messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze how topics evolve throughout the discussion."""
        # Split discussion into time windows
        window_size = max(1, len(messages) // 4)  # 4 windows minimum
        windows = [
            messages[i:i+window_size]
            for i in range(0, len(messages), window_size)
        ]
        
        topic_evolution = []
        for window in windows:
            combined_text = " ".join(msg["content"] for msg in window)
            
            # Analyze window content
            window_analysis = {
                "timestamp_start": window[0]["timestamp"],
                "timestamp_end": window[-1]["timestamp"],
                "key_terms": self.word_processor._get_keyword_frequency(
                    self.word_processor._tokenize(combined_text)
                ),
                "sentiment": self.word_processor._analyze_sentiment(
                    combined_text
                ),
                "key_points": self.word_processor.extract_key_points(
                    combined_text,
                    num_points=2
                )
            }
            topic_evolution.append(window_analysis)
            
        return {
            "windows": topic_evolution,
            "topic_shifts": self._detect_topic_shifts(topic_evolution)
        }
        
    def _analyze_engagement(
        self,
        messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze participant engagement levels."""
        engagement_metrics = defaultdict(lambda: {
            "message_frequency": [],
            "content_richness": [],
            "interaction_score": 0,
            "contribution_impact": []
        })
        
        # Calculate metrics per participant
        for msg in messages:
            sender = msg["sender"]
            content = msg["content"]
            
            # Content richness based on length and unique words
            words = set(self.word_processor._tokenize(content))
            richness_score = len(words) / max(1, len(content.split()))
            engagement_metrics[sender]["content_richness"].append(richness_score)
            
            # Contribution impact based on responses
            impact_score = self._calculate_impact_score(msg, messages)
            engagement_metrics[sender]["contribution_impact"].append(impact_score)
            
        # Calculate time-based metrics
        for participant in engagement_metrics:
            metrics = engagement_metrics[participant]
            if metrics["content_richness"]:
                metrics["avg_richness"] = (
                    sum(metrics["content_richness"]) /
                    len(metrics["content_richness"])
                )
            if metrics["contribution_impact"]:
                metrics["avg_impact"] = (
                    sum(metrics["contribution_impact"]) /
                    len(metrics["contribution_impact"])
                )
                
        return dict(engagement_metrics)
        
    def _analyze_discussion_flow(
        self,
        messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze the flow and coherence of discussion."""
        flow_metrics = {
            "topic_coherence": [],
            "turn_taking": [],
            "response_chains": []
        }
        
        for i in range(1, len(messages)):
            prev_msg = messages[i-1]
            curr_msg = messages[i]
            
            # Analyze topic coherence
            coherence = self._calculate_coherence(
                prev_msg["content"],
                curr_msg["content"]
            )
            flow_metrics["topic_coherence"].append(coherence)
            
            # Analyze turn-taking patterns
            if prev_msg["sender"] != curr_msg["sender"]:
                flow_metrics["turn_taking"].append({
                    "from": prev_msg["sender"],
                    "to": curr_msg["sender"],
                    "timestamp": curr_msg["timestamp"]
                })
                
            # Track response chains
            if i >= 2:
                chain = self._identify_response_chain(
                    messages[i-2:i+1]
                )
                if chain:
                    flow_metrics["response_chains"].append(chain)
                    
        return flow_metrics
        
    def _has_reference(self, text1: str, text2: str) -> bool:
        """Check if one text references another."""
        words1 = set(self.word_processor._tokenize(text1))
        words2 = set(self.word_processor._tokenize(text2))
        return len(words1 & words2) >= 3  # At least 3 common words
        
    def _detect_topic_shifts(
        self,
        topic_evolution: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Detect significant shifts in discussion topics."""
        shifts = []
        for i in range(1, len(topic_evolution)):
            prev_terms = set(topic_evolution[i-1]["key_terms"].keys())
            curr_terms = set(topic_evolution[i]["key_terms"].keys())
            
            # Calculate topic shift magnitude
            similarity = len(prev_terms & curr_terms) / max(
                1,
                len(prev_terms | curr_terms)
            )
            
            if similarity < 0.3:  # Significant shift threshold
                shifts.append({
                    "timestamp": topic_evolution[i]["timestamp_start"],
                    "previous_topics": list(prev_terms),
                    "new_topics": list(curr_terms),
                    "shift_magnitude": 1 - similarity
                })
                
        return shifts
        
    def _calculate_impact_score(
        self,
        message: Dict[str, Any],
        all_messages: List[Dict[str, Any]]
    ) -> float:
        """Calculate the impact score of a message."""
        msg_time = datetime.fromisoformat(message["timestamp"])
        response_count = 0
        content_similarity = 0
        
        # Look at messages within next 5 minutes
        for msg in all_messages:
            curr_time = datetime.fromisoformat(msg["timestamp"])
            if curr_time > msg_time and (
                curr_time - msg_time
            ) <= timedelta(minutes=5):
                response_count += 1
                if self._has_reference(msg["content"], message["content"]):
                    content_similarity += 1
                    
        return (response_count + content_similarity) / 2
        
    def _calculate_coherence(self, text1: str, text2: str) -> float:
        """Calculate coherence between two messages."""
        words1 = set(self.word_processor._tokenize(text1))
        words2 = set(self.word_processor._tokenize(text2))
        
        if not words1 or not words2:
            return 0.0
            
        common_words = len(words1 & words2)
        total_words = len(words1 | words2)
        
        return common_words / total_words
        
    def _identify_response_chain(
        self,
        messages: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Identify a response chain in messages."""
        if len(messages) < 3:
            return None
            
        # Check if messages form a coherent chain
        coherence_scores = [
            self._calculate_coherence(
                messages[i]["content"],
                messages[i+1]["content"]
            )
            for i in range(len(messages)-1)
        ]
        
        if all(score > 0.2 for score in coherence_scores):
            return {
                "participants": [msg["sender"] for msg in messages],
                "start_time": messages[0]["timestamp"],
                "end_time": messages[-1]["timestamp"],
                "coherence_score": sum(coherence_scores) / len(coherence_scores)
            }
            
        return None
