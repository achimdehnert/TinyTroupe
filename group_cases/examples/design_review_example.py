"""
Example of running a design review for a new web application interface.
"""
from group_cases.src.discussions.design_review import DesignReviewDiscussion

def main():
    # Create design review for a new e-commerce checkout flow
    discussion = DesignReviewDiscussion(
        design_name="Checkout Flow Redesign",
        design_type="UI/UX"
    )
    
    # Add context about the design
    discussion.add_context("current_pain_points", [
        "High cart abandonment rate",
        "Confusion about shipping options",
        "Payment method selection unclear"
    ])
    
    discussion.add_context("design_goals", [
        "Reduce checkout steps from 5 to 3",
        "Improve mobile responsiveness",
        "Add express checkout option",
        "Better error handling and validation"
    ])
    
    discussion.add_context("user_research", {
        "user_tests": 15,
        "key_findings": [
            "Users want progress indication",
            "Address form is too long",
            "Payment options are hard to find"
        ]
    })
    
    # Run review
    results = discussion.run_discussion(num_steps=5)
    
    # Save results
    discussion.save_results(
        results,
        "data/extractions/checkout_design_review.json"
    )

if __name__ == "__main__":
    main()
