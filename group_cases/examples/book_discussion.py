"""
Example script demonstrating a discussion about evaluating a new book idea.
"""
from ..src.core.discussion_manager import DiscussionManager
from ..src.core.base_discussion import BaseDiscussion, DiscussionType

class BookDiscussion(BaseDiscussion):
    """Discussion about evaluating and developing a book idea."""
    
    def __init__(self):
        self.name = "Book Concept Evaluation"
        self.discussion_type = DiscussionType.BRAINSTORMING
        self.context = {
            "concept": "A science fiction novel about a society where dreams can be recorded and traded",
            "target_audience": "Young Adult and Adult readers",
            "genre": "Science Fiction / Psychological Thriller",
            "key_themes": [
                "Privacy in digital age",
                "Commodification of human experiences",
                "Ethics of consciousness manipulation"
            ]
        }

def main():
    try:
        # Create discussion instance
        discussion = BookDiscussion()
        manager = DiscussionManager(discussion)
        
        # Setup agents with different expertise
        roles = [
            {
                "name": "Literary Agent",
                "role": "Evaluate market potential and positioning",
                "traits": ["analytical", "market-savvy", "experienced"]
            },
            {
                "name": "Editor",
                "role": "Assess narrative structure and storytelling elements",
                "traits": ["detail-oriented", "creative", "critical"]
            },
            {
                "name": "SciFi Author",
                "role": "Evaluate genre elements and world-building",
                "traits": ["imaginative", "technical", "genre-expert"]
            },
            {
                "name": "Marketing Specialist",
                "role": "Consider audience appeal and marketing angles",
                "traits": ["trend-aware", "strategic", "audience-focused"]
            }
        ]
        manager.setup_agents(roles)
        
        # Define discussion steps
        steps = [
            {
                "phase": "concept_evaluation",
                "previous_results": [],
                "discussion_context": {
                    "focus": "Core Concept Viability",
                    "questions": [
                        "How unique is this concept in the current market?",
                        "What are the strongest narrative possibilities?",
                        "What potential challenges might arise in execution?"
                    ]
                }
            },
            {
                "phase": "market_analysis",
                "previous_results": [],
                "discussion_context": {
                    "focus": "Market Potential",
                    "criteria": [
                        "Target audience reach",
                        "Genre market trends",
                        "Competitive landscape",
                        "Marketing opportunities"
                    ]
                }
            },
            {
                "phase": "development_recommendations",
                "previous_results": [],
                "discussion_context": {
                    "focus": "Next Steps",
                    "areas": [
                        "Story development priorities",
                        "World-building elements",
                        "Character dynamics",
                        "Marketing strategy"
                    ]
                }
            }
        ]
        
        # Run each step and collect insights
        previous_results = []
        for i, step in enumerate(steps, 1):
            print(f"\nStep {i}: {step['phase'].title()}")
            print("-" * 50)
            
            if i > 1:
                step["previous_results"] = previous_results
            
            try:
                results = manager.run_step(step)
                previous_results = results.get("responses", [])
                
                print("\nInsights:")
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
