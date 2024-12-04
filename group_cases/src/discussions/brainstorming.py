"""
Specialized discussion implementation for brainstorming sessions.
"""
from typing import Dict, List, Any, Optional
from ..core.base_discussion import BaseDiscussion, DiscussionType
from ..core.discussion_manager import DiscussionManager

class BrainstormingDiscussion(BaseDiscussion):
    """Implementation of brainstorming-specific discussion logic."""
    
    def __init__(self, topic: str, domain: str):
        """
        Initialize brainstorming discussion.
        
        Args:
            topic: Topic to brainstorm about
            domain: Domain/industry context
        """
        super().__init__(f"{topic} Brainstorming", DiscussionType.BRAINSTORMING)
        self.topic = topic
        self.domain = domain
        self.add_metadata("topic", topic)
        self.add_metadata("domain", domain)
        
    def run_discussion(self, num_steps: int = 3) -> Dict[str, Any]:
        """
        Run the brainstorming session.
        
        Args:
            num_steps: Number of discussion rounds
            
        Returns:
            Brainstorming results
        """
        manager = DiscussionManager(self)
        
        # Setup roles for brainstorming
        roles = [
            {"name": "Facilitator", "role": "Guide discussion and ensure focus"},
            {"name": "Innovator", "role": "Generate creative ideas"},
            {"name": "Critic", "role": "Evaluate feasibility"},
            {"name": "Domain Expert", "role": f"Provide expertise in {self.domain}"}
        ]
        manager.setup_agents(roles)
        
        results = []
        for step in range(num_steps):
            step_config = {
                "phase": "ideation" if step < num_steps-1 else "consolidation",
                "context": self.context,
                "previous_results": results
            }
            step_result = manager.run_step(step_config)
            results.append(step_result)
            
        return manager.extract_results(results)
