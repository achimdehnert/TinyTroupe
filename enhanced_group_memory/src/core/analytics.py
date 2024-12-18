"""
Advanced analytics for discussions and memory analysis.
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta
import numpy as np
from textblob import TextBlob
from .discussion import Message, MessageType
from .memory import Memory

class DiscussionAnalytics:
    @staticmethod
    def analyze_sentiment(text: str) -> float:
        """Analyze sentiment of text using TextBlob."""
        blob = TextBlob(text)
        return blob.sentiment.polarity
    
    @staticmethod
    def analyze_message_patterns(messages: List[Message]) -> Dict[str, Any]:
        """Analyze patterns in message timing and length."""
        if not messages:
            return {}
        
        # Message timing analysis
        timestamps = [msg.timestamp for msg in messages]
        time_diffs = np.diff([ts.timestamp() for ts in timestamps])
        
        # Message length analysis
        lengths = [len(msg.content) for msg in messages]
        
        return {
            "avg_time_between_messages": float(np.mean(time_diffs)) if len(time_diffs) > 0 else 0,
            "max_time_between_messages": float(np.max(time_diffs)) if len(time_diffs) > 0 else 0,
            "avg_message_length": float(np.mean(lengths)),
            "max_message_length": max(lengths),
            "min_message_length": min(lengths)
        }
    
    @staticmethod
    def analyze_user_engagement(messages: List[Message]) -> Dict[str, Any]:
        """Analyze user engagement patterns."""
        user_stats = {}
        
        for msg in messages:
            if msg.sender not in user_stats:
                user_stats[msg.sender] = {
                    "message_count": 0,
                    "total_length": 0,
                    "reactions_received": 0,
                    "reactions_given": 0,
                    "avg_sentiment": []
                }
            
            stats = user_stats[msg.sender]
            stats["message_count"] += 1
            stats["total_length"] += len(msg.content)
            stats["reactions_received"] += sum(len(users) for users in msg.reactions.values())
            stats["avg_sentiment"].append(DiscussionAnalytics.analyze_sentiment(msg.content))
        
        # Calculate averages
        for user, stats in user_stats.items():
            stats["avg_message_length"] = stats["total_length"] / stats["message_count"]
            stats["avg_sentiment"] = np.mean(stats["avg_sentiment"])
            
        return user_stats
    
    @staticmethod
    def analyze_memory_patterns(memories: List[Memory]) -> Dict[str, Any]:
        """Analyze patterns in memory formation and recall."""
        if not memories:
            return {}
            
        # Time-based analysis
        timestamps = [m.timestamp for m in memories]
        memory_age = [(datetime.now() - ts).total_seconds() for ts in timestamps]
        
        # Context analysis
        contexts = [set(m.context.keys()) for m in memories]
        common_contexts = set.intersection(*contexts) if contexts else set()
        
        return {
            "total_memories": len(memories),
            "avg_memory_age": float(np.mean(memory_age)),
            "oldest_memory_age": float(np.max(memory_age)),
            "newest_memory_age": float(np.min(memory_age)),
            "common_context_keys": list(common_contexts)
        }
    
    @staticmethod
    def generate_summary_report(
        messages: List[Message],
        memories: List[Memory]
    ) -> Dict[str, Any]:
        """Generate a comprehensive analytics report."""
        message_patterns = DiscussionAnalytics.analyze_message_patterns(messages)
        user_engagement = DiscussionAnalytics.analyze_user_engagement(messages)
        memory_patterns = DiscussionAnalytics.analyze_memory_patterns(memories)
        
        # Overall sentiment analysis
        all_sentiments = [
            DiscussionAnalytics.analyze_sentiment(msg.content)
            for msg in messages
        ]
        
        return {
            "message_patterns": message_patterns,
            "user_engagement": user_engagement,
            "memory_patterns": memory_patterns,
            "overall_sentiment": {
                "average": float(np.mean(all_sentiments)) if all_sentiments else 0,
                "variance": float(np.var(all_sentiments)) if all_sentiments else 0,
                "trend": "positive" if np.mean(all_sentiments) > 0 else "negative"
            }
        }
