"""
Specialized discussion implementation for interview sessions.
"""
from typing import Dict, List, Any, Optional
from ..core.base_discussion import BaseDiscussion, DiscussionType
from ..core.discussion_manager import DiscussionManager

class InterviewDiscussion(BaseDiscussion):
    """Implementation of interview-specific discussion logic."""
    
    def __init__(self, interviewee_type: str, objective: str):
        """
        Initialize interview discussion.
        
        Args:
            interviewee_type: Type/role of the interviewee
            objective: Main objective of the interview
        """
        super().__init__(f"{interviewee_type} Interview", DiscussionType.INTERVIEW)
        self.interviewee_type = interviewee_type
        self.objective = objective
        self.add_metadata("interviewee_type", interviewee_type)
        self.add_metadata("objective", objective)
        
    def run_discussion(self, num_steps: int = 3) -> Dict[str, Any]:
        """
        Run the interview session.
        
        Args:
            num_steps: Number of interview segments
            
        Returns:
            Interview results
        """
        manager = DiscussionManager(self)
        
        # Setup roles for interview
        roles = [
            {"name": "Interviewer", "role": "Lead the interview"},
            {"name": "Interviewee", "role": f"Act as {self.interviewee_type}"},
            {"name": "Observer", "role": "Note key insights"},
            {"name": "Follow-up", "role": "Ask clarifying questions"}
        ]
        manager.setup_agents(roles)
        
        results = []
        for step in range(num_steps):
            step_config = {
                "phase": ["opening", "deep-dive", "closing"][min(step, 2)],
                "context": self.context,
                "previous_results": results
            }
            step_result = manager.run_step(step_config)
            results.append(step_result)
            
        return manager.extract_results(results)
