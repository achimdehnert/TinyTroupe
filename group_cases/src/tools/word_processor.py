"""
Word processing tools for discussion content management.
"""
from typing import Dict, List, Any, Optional
import re
from collections import Counter
from datetime import datetime

class WordProcessor:
    """Processor for discussion content analysis and manipulation."""
    
    def __init__(self):
        """Initialize word processor."""
        self.stop_words = set([
            "a", "an", "and", "are", "as", "at", "be", "by", "for",
            "from", "has", "he", "in", "is", "it", "its", "of", "on",
            "that", "the", "to", "was", "were", "will", "with"
        ])
        
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text content.
        
        Args:
            text: Text to analyze
            
        Returns:
            Analysis results
        """
        words = self._tokenize(text)
        word_count = len(words)
        unique_words = len(set(words))
        
        return {
            "word_count": word_count,
            "unique_words": unique_words,
            "avg_word_length": self._average_word_length(words),
            "keyword_frequency": self._get_keyword_frequency(words),
            "readability_score": self._calculate_readability(text),
            "sentiment_indicators": self._analyze_sentiment(text)
        }
        
    def extract_key_points(self, text: str, num_points: int = 3) -> List[str]:
        """
        Extract key points from text.
        
        Args:
            text: Source text
            num_points: Number of key points to extract
            
        Returns:
            List of key points
        """
        sentences = self._split_sentences(text)
        scored_sentences = [
            (s, self._score_sentence(s))
            for s in sentences
        ]
        
        # Sort by score and get top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored_sentences[:num_points]]
        
    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """
        Generate text summary.
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length
            
        Returns:
            Generated summary
        """
        key_points = self.extract_key_points(text)
        summary = " ".join(key_points)
        
        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."
            
        return summary
        
    def format_discussion(
        self,
        messages: List[Dict[str, Any]],
        format_type: str = "markdown"
    ) -> str:
        """
        Format discussion messages.
        
        Args:
            messages: List of discussion messages
            format_type: Output format type
            
        Returns:
            Formatted discussion content
        """
        if format_type == "markdown":
            return self._format_markdown(messages)
        elif format_type == "html":
            return self._format_html(messages)
        else:
            return self._format_plain(messages)
            
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        # Convert to lowercase and split
        words = text.lower().split()
        
        # Remove punctuation and filter stop words
        words = [
            re.sub(r'[^\w\s]', '', word)
            for word in words
        ]
        return [
            w for w in words
            if w and w not in self.stop_words
        ]
        
    def _average_word_length(self, words: List[str]) -> float:
        """Calculate average word length."""
        if not words:
            return 0.0
        return sum(len(w) for w in words) / len(words)
        
    def _get_keyword_frequency(self, words: List[str]) -> Dict[str, int]:
        """Get frequency of keywords."""
        word_freq = Counter(words)
        # Return top 10 most common words
        return dict(word_freq.most_common(10))
        
    def _calculate_readability(self, text: str) -> float:
        """Calculate text readability score."""
        sentences = self._split_sentences(text)
        if not sentences:
            return 0.0
            
        words = self._tokenize(text)
        if not words:
            return 0.0
            
        # Simple readability score based on average sentence length
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = self._average_word_length(words)
        
        # Score between 0 and 1, lower is more readable
        return min(1.0, (avg_sentence_length * avg_word_length) / 100)
        
    def _analyze_sentiment(self, text: str) -> Dict[str, int]:
        """Analyze text sentiment indicators."""
        positive_words = {"good", "great", "excellent", "positive", "agree"}
        negative_words = {"bad", "poor", "negative", "disagree", "issue"}
        
        words = set(self._tokenize(text))
        
        return {
            "positive": len(words & positive_words),
            "negative": len(words & negative_words)
        }
        
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
        
    def _score_sentence(self, sentence: str) -> float:
        """Score sentence importance."""
        words = self._tokenize(sentence)
        
        # Factors in scoring:
        # 1. Length (not too short, not too long)
        length_score = min(1.0, len(words) / 20.0)
        
        # 2. Keyword presence
        keyword_indicators = {
            "important", "key", "significant", "main", "critical",
            "essential", "crucial", "primary", "major", "vital"
        }
        keyword_score = len(set(words) & keyword_indicators) * 0.2
        
        # 3. Position bonus (if available in original text)
        position_score = 0.1  # Default position score
        
        return length_score + keyword_score + position_score
        
    def _format_markdown(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages in markdown."""
        output = []
        current_date = None
        
        for msg in messages:
            # Add date header if new date
            msg_date = datetime.fromisoformat(
                msg["timestamp"]
            ).date()
            if msg_date != current_date:
                current_date = msg_date
                output.append(f"\n## {current_date}\n")
            
            # Format message
            sender = msg["sender"]
            content = msg["content"]
            time = datetime.fromisoformat(
                msg["timestamp"]
            ).strftime("%H:%M")
            
            output.append(
                f"**{sender}** ({time}): {content}"
            )
            
        return "\n".join(output)
        
    def _format_html(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages in HTML."""
        output = ['<div class="discussion">']
        current_date = None
        
        for msg in messages:
            # Add date header if new date
            msg_date = datetime.fromisoformat(
                msg["timestamp"]
            ).date()
            if msg_date != current_date:
                current_date = msg_date
                output.append(
                    f'<h2 class="date-header">{current_date}</h2>'
                )
            
            # Format message
            sender = msg["sender"]
            content = msg["content"]
            time = datetime.fromisoformat(
                msg["timestamp"]
            ).strftime("%H:%M")
            
            output.append(
                f'<div class="message">'
                f'<span class="sender">{sender}</span> '
                f'<span class="time">({time})</span>: '
                f'<span class="content">{content}</span>'
                f'</div>'
            )
            
        output.append('</div>')
        return "\n".join(output)
        
    def _format_plain(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages in plain text."""
        output = []
        current_date = None
        
        for msg in messages:
            # Add date header if new date
            msg_date = datetime.fromisoformat(
                msg["timestamp"]
            ).date()
            if msg_date != current_date:
                current_date = msg_date
                output.append(f"\n=== {current_date} ===\n")
            
            # Format message
            sender = msg["sender"]
            content = msg["content"]
            time = datetime.fromisoformat(
                msg["timestamp"]
            ).strftime("%H:%M")
            
            output.append(f"[{time}] {sender}: {content}")
            
        return "\n".join(output)
