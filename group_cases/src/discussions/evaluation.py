"""
Specialized discussion implementation for evaluation sessions.
"""
from typing import Dict, List, Any, Optional
from ..core.base_discussion import BaseDiscussion, DiscussionType
from ..core.discussion_manager import DiscussionManager

class EvaluationDiscussion(BaseDiscussion):
    """Implementation of evaluation-specific discussion logic."""
    
    def __init__(self, subject: str, criteria: List[str]):
        """
        Initialize evaluation discussion.
        
        Args:
            subject: Subject to evaluate
            criteria: List of evaluation criteria
        """
        super().__init__(f"{subject} Evaluation", DiscussionType.EVALUATION)
        self.subject = subject
        self.criteria = criteria
        self.add_metadata("subject", subject)
        self.add_metadata("criteria", criteria)
        
    def run_discussion(self, num_steps: int = 3) -> Dict[str, Any]:
        """
        Run the evaluation session.
        
        Args:
            num_steps: Number of evaluation rounds
            
        Returns:
            Evaluation results
        """
        manager = DiscussionManager(self)
        
        # Setup roles for evaluation
        roles = [
            {"name": "Moderator", "role": "Guide evaluation process"},
            {"name": "Evaluator", "role": "Assess based on criteria"},
            {"name": "Devil's Advocate", "role": "Challenge assumptions"},
            {"name": "Synthesizer", "role": "Combine perspectives"}
        ]
        manager.setup_agents(roles)
        
        results = []
        for step in range(num_steps):
            criteria_subset = self.criteria[step::num_steps]
            step_config = {
                "criteria": criteria_subset,
                "context": self.context,
                "previous_results": results
            }
            step_result = manager.run_step(step_config)
            results.append(step_result)
            
        return manager.extract_results(results)
