#!/usr/bin/env python
# coding: utf-8

import sys
import os
sys.path.append('..')

from group_cases.src.group_discussion import ProductBrainstormingDiscussion

def main():
    # Create brainstorming session for Microsoft Word
    discussion = ProductBrainstormingDiscussion(
        "Microsoft Word",
        "office productivity"
    )
    
    # Add specific context about current features and target users
    discussion.add_context("current_features", [
        "text editing",
        "formatting",
        "spell check",
        "grammar check",
        "track changes",
        "comments"
    ])
    discussion.add_context("target_users", [
        "writers",
        "business professionals",
        "students",
        "academics"
    ])
    
    # Run discussion with more steps for deeper exploration
    results = discussion.run_discussion(num_steps=4)
    
    # Save results
    discussion.save_results(
        results,
        "data/extractions/word_features.extraction.json"
    )

if __name__ == "__main__":
    main()
