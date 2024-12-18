"""
Example script demonstrating the DiscussionManager in action.
"""
from group_cases.src.core.discussion_manager import DiscussionManager
from group_cases.src.core.base_discussion import BaseDiscussion, DiscussionType

class ProductDiscussion(BaseDiscussion):
    """Example discussion about product features."""
    
    def __init__(self):
        self.name = "Product Feature Discussion"
        self.discussion_type = DiscussionType.BRAINSTORMING
        self.context = {
            "product": "Mobile App",
            "current_features": ["User Authentication", "Profile Management"],
            "target_audience": "Young Professionals",
            "objectives": ["Improve User Engagement", "Add Social Features"]
        }

def main():
    try:
        # Create discussion instance
        discussion = ProductDiscussion()
        manager = DiscussionManager(discussion)
        
        # Setup agents with different roles
        roles = [
            {"name": "Moderator", "role": "Guide the discussion and ensure all perspectives are heard"},
            {"name": "Product Manager", "role": "Focus on user needs and market fit"},
            {"name": "UX Designer", "role": "Consider user experience and interface design"},
            {"name": "Developer", "role": "Evaluate technical feasibility"}
        ]
        manager.setup_agents(roles)
        
        # Run discussion steps
        steps = [
            {
                "phase": "ideation",
                "previous_results": [],
                "discussion_context": {
                    "focus": "Social Features",
                    "constraints": ["Must be implementable in 2 months", "Should leverage existing user data"]
                }
            },
            {
                "phase": "evaluation",
                "previous_results": [],  # Will be filled with results from previous step
                "discussion_context": {
                    "focus": "Feature Prioritization",
                    "criteria": ["User Value", "Development Effort", "Market Impact"]
                }
            }
        ]
        
        # Run each step and print results
        previous_results = []
        for i, step in enumerate(steps, 1):
            print(f"\nStep {i}: {step['phase'].title()}")
            print("-" * 50)
            
            if i > 1:
                # Add previous step results
                step["previous_results"] = previous_results
            
            try:
                results = manager.run_step(step)
                previous_results = results.get("responses", [])
                
                print("\nResponses:")
                for response in results.get("responses", []):
                    print(f"\n{response.get('agent', '')}:")
                    print(response.get('response', ''))
                
                print("\nSummary:")
                print(results.get("summary", ''))
            except Exception as e:
                print(f"Error during step {i}: {str(e)}")
                continue

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
