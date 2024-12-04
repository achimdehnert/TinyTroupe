"""
Base discussion module providing core functionality for all discussion types.
"""
from enum import Enum
import json
import os
from typing import Any, Dict, List, Optional

class DiscussionType(Enum):
    FOCUS_GROUP = "focus_group"
    INTERVIEW = "interview"
    BRAINSTORMING = "brainstorming"
    EVALUATION = "evaluation"

class BaseDiscussion:
    """Base class for all discussion types."""
    
    def __init__(self, name: str, discussion_type: DiscussionType):
        """
        Initialize base discussion.
        
        Args:
            name: Name/identifier for the discussion
            discussion_type: Type of discussion from DiscussionType enum
        """
        self.name = name
        self.discussion_type = discussion_type
        self.context: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {
            "name": name,
            "type": discussion_type.value
        }
        
    def add_context(self, key: str, value: Any) -> None:
        """Add context information to the discussion."""
        self.context[key] = value
        
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata information."""
        self.metadata[key] = value
        
    def prepare_extraction_config(self) -> Dict[str, Any]:
        """Prepare configuration for result extraction."""
        return {
            "context": self.context,
            "metadata": self.metadata
        }
        
    def save_results(self, results: Dict[str, Any], filepath: str) -> None:
        """Save discussion results to file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "results": results,
                "metadata": self.metadata,
                "context": self.context
            }, f, indent=2)
            
    def run_discussion(self, num_steps: int = 3) -> Dict[str, Any]:
        """
        Run the discussion. Should be implemented by subclasses.
        
        Args:
            num_steps: Number of discussion steps
            
        Returns:
            Discussion results
        """
        raise NotImplementedError("Subclasses must implement run_discussion()")
