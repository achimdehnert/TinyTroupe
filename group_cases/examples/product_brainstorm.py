#!/usr/bin/env python
# coding: utf-8

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.group_discussion import ProductBrainstormingDiscussion

def main():
    # Create and run brainstorming session
    discussion = ProductBrainstormingDiscussion(
        "Visual Studio Code",
        "software development"
    )
    
    # Add specific context
    discussion.add_context("target_users", "developers")
    discussion.add_context("current_features", [
        "syntax highlighting",
        "debugging",
        "source control",
        "extensions"
    ])
    
    # Run discussion
    results = discussion.run_discussion(num_steps=4)
    
    # Save results
    output_file = os.path.join(
        os.path.dirname(__file__), 
        '../data/extractions/vscode_features.json'
    )
    discussion.save_results(results, output_file)

if __name__ == "__main__":
    main()
