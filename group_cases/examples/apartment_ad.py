#!/usr/bin/env python
# coding: utf-8

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.group_discussion import ApartmentAdDiscussion

def main():
    # Apartment description
    apartment_desc = """
    Luxury 1-bedroom apartment features:
    - Fully renovated by top architect
    - Integrated, open-concept spaces
    - Modern kitchen with 60s-style chairs
    - Home office conversion
    - 2 elegant bathrooms
    - New appliances including washer/dryer
    - Fully furnished
    - Prime location near medical school
    - Quiet despite main avenue location
    - Close to supermarket, restaurants, and transport
    """
    
    # Create and run discussion
    discussion = ApartmentAdDiscussion(apartment_desc)
    results = discussion.run_discussion()
    
    # Save results
    output_file = os.path.join(
        os.path.dirname(__file__), 
        '../data/extractions/luxury_apartment_ad.json'
    )
    discussion.save_results(results, output_file)

if __name__ == "__main__":
    main()
