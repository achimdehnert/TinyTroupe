"""
Specialized discussion implementation for design review sessions.
"""
from typing import Dict, List, Any, Optional
from ..core.base_discussion import BaseDiscussion, DiscussionType
from ..core.discussion_manager import DiscussionManager

class DesignReviewDiscussion(BaseDiscussion):
    """Implementation of design review-specific discussion logic."""
    
    def __init__(self, design_name: str, design_type: str):
        """
        Initialize design review discussion.
        
        Args:
            design_name: Name of the design to review
            design_type: Type of design (UI/UX, architecture, etc.)
        """
        super().__init__(f"{design_name} Design Review", DiscussionType.EVALUATION)
        self.design_name = design_name
        self.design_type = design_type
        self.add_metadata("design_name", design_name)
        self.add_metadata("design_type", design_type)
        
    def run_discussion(self, num_steps: int = 3) -> Dict[str, Any]:
        """
        Run the design review session.
        
        Args:
            num_steps: Number of review segments
            
        Returns:
            Design review results
        """
        manager = DiscussionManager(self)
        
        # Setup roles for design review
        roles = [
            {"name": "ReviewLead", "role": "Guide the review process"},
            {"name": "Designer", "role": "Present and explain design decisions"},
            {"name": "TechnicalReviewer", "role": "Assess technical feasibility"},
            {"name": "UserAdvocate", "role": "Evaluate from user perspective"}
        ]
        manager.setup_agents(roles)
        
        results = []
        review_aspects = [
            "design_principles",
            "usability",
            "technical_feasibility",
            "accessibility",
            "scalability"
        ]
        
        for step in range(num_steps):
            aspects = review_aspects[step::num_steps]
            step_config = {
                "aspects": aspects,
                "context": self.context,
                "previous_results": results,
                "review_criteria": self.get_review_criteria(aspects)
            }
            step_result = manager.run_step(step_config)
            results.append(step_result)
            
        return manager.extract_results(results)
    
    def get_review_criteria(self, aspects: List[str]) -> Dict[str, List[str]]:
        """Get review criteria for each aspect."""
        criteria_map = {
            "design_principles": ["consistency", "clarity", "hierarchy"],
            "usability": ["ease of use", "learnability", "efficiency"],
            "technical_feasibility": ["implementation complexity", "performance", "maintainability"],
            "accessibility": ["screen readers", "keyboard navigation", "color contrast"],
            "scalability": ["load handling", "extensibility", "modularity"]
        }
        return {aspect: criteria_map.get(aspect, []) for aspect in aspects}
