"""
Specialized discussion implementation for focus group sessions.
"""
from typing import Dict, List, Any, Optional
from ..core.base_discussion import BaseDiscussion, DiscussionType
from ..core.discussion_manager import DiscussionManager

class FocusGroupDiscussion(BaseDiscussion):
    """Implementation of focus group-specific discussion logic."""
    
    def __init__(self, topic: str, target_demographic: str):
        """
        Initialize focus group discussion.
        
        Args:
            topic: Topic for discussion
            target_demographic: Target demographic group
        """
        super().__init__(f"{topic} Focus Group", DiscussionType.FOCUS_GROUP)
        self.topic = topic
        self.target_demographic = target_demographic
        self.add_metadata("topic", topic)
        self.add_metadata("target_demographic", target_demographic)
        
    def run_discussion(self, num_steps: int = 3) -> Dict[str, Any]:
        """
        Run the focus group session.
        
        Args:
            num_steps: Number of discussion segments
            
        Returns:
            Focus group results
        """
        manager = DiscussionManager(self)
        
        # Setup roles for focus group
        roles = [
            {"name": "Moderator", "role": "Guide discussion and ensure equal participation"},
            {"name": "Consumer1", "role": f"Representative of {self.target_demographic}, perspective 1"},
            {"name": "Consumer2", "role": f"Representative of {self.target_demographic}, perspective 2"},
            {"name": "Observer", "role": "Record group dynamics and key insights"}
        ]
        manager.setup_agents(roles)
        
        results = []
        discussion_phases = [
            "warmup",
            "main_discussion",
            "deep_dive",
            "wrap_up"
        ]
        
        for step in range(num_steps):
            phase = discussion_phases[min(step, len(discussion_phases)-1)]
            step_config = {
                "phase": phase,
                "context": self.context,
                "previous_results": results,
                "focus_points": self.get_focus_points(phase)
            }
            step_result = manager.run_step(step_config)
            results.append(step_result)
            
        return manager.extract_results(results)
    
    def get_focus_points(self, phase: str) -> List[str]:
        """Get focus points for each discussion phase."""
        focus_points = {
            "warmup": ["general impressions", "initial thoughts"],
            "main_discussion": ["key features", "use cases", "pain points"],
            "deep_dive": ["specific scenarios", "detailed feedback"],
            "wrap_up": ["final thoughts", "recommendations"]
        }
        return focus_points.get(phase, [])
