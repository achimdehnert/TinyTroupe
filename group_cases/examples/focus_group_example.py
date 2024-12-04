"""
Example of running a focus group discussion about a new smartphone app.
"""
from group_cases.src.discussions.focus_group import FocusGroupDiscussion

def main():
    # Create focus group for a new fitness tracking app
    discussion = FocusGroupDiscussion(
        topic="FitTrack Pro App",
        target_demographic="health-conscious millennials"
    )
    
    # Add context about the product
    discussion.add_context("product_features", [
        "AI-powered workout recommendations",
        "Social fitness challenges",
        "Nutrition tracking",
        "Integration with wearables"
    ])
    
    discussion.add_context("competitor_products", [
        "MyFitnessPal",
        "Strava",
        "Nike Training Club"
    ])
    
    # Run discussion
    results = discussion.run_discussion(num_steps=4)
    
    # Save results
    discussion.save_results(
        results,
        "data/extractions/fittrack_focus_group.json"
    )

if __name__ == "__main__":
    main()
