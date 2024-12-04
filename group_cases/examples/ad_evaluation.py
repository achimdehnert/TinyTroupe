#!/usr/bin/env python
# coding: utf-8

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.group_discussion import AdEvaluationDiscussion

def main():
    # Sample ads to evaluate
    ads = [
        """
        Transform Your Workspace with AI-Powered Productivity
        Experience the future of work with our revolutionary AI assistant.
        - Real-time task prioritization
        - Smart meeting scheduling
        - Automated email management
        - Personalized productivity insights
        Start your free trial today and boost your efficiency by 40%!
        """,
        
        """
        Work Smarter, Not Harder
        Let our AI handle the routine while you focus on what matters.
        ✓ Intelligent task management
        ✓ Calendar optimization
        ✓ Email automation
        ✓ Performance analytics
        Join 10,000+ professionals who've revolutionized their workflow.
        """
    ]
    
    # Create and run evaluation
    discussion = AdEvaluationDiscussion("Productivity Software", ads)
    results = discussion.run_discussion(reduce_results=True)
    
    # Save results
    output_file = os.path.join(
        os.path.dirname(__file__), 
        '../data/extractions/productivity_ads_evaluation.json'
    )
    discussion.save_results(results, output_file)

if __name__ == "__main__":
    main()
