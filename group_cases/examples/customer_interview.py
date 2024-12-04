#!/usr/bin/env python
# coding: utf-8

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.group_discussion import CustomerInterviewDiscussion

def main():
    # Company context and customer profile
    company_context = """
    Leading fintech startup disrupting traditional banking with AI-powered
    solutions. Growing rapidly but facing challenges in enterprise adoption
    and regulatory compliance.
    """
    
    customer_profile = """
    Chief Technology Officer at a Fortune 500 bank with 20 years of experience.
    Responsible for digital transformation initiatives and vendor selection.
    Conservative approach to new technology adoption due to regulatory requirements.
    """
    
    # Create and run interview
    discussion = CustomerInterviewDiscussion(company_context, customer_profile)
    results = discussion.run_discussion(num_steps=5)
    
    # Save results
    output_file = os.path.join(
        os.path.dirname(__file__), 
        '../data/extractions/enterprise_cto_interview.json'
    )
    discussion.save_results(results, output_file)

if __name__ == "__main__":
    main()
