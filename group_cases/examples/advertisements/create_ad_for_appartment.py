#!/usr/bin/env python
# coding: utf-8

import sys
import os
sys.path.append('..')

from group_cases.src.group_discussion import ApartmentAdDiscussion

def main():
    # Apartment description with all details
    apartment_desc = """	
    The appartment has the following characteristics:
      - It is in an old building, but was completely renovated and remodeled by an excellent architect. 
        There are almost no walls, so it is very spacious, mostly composed of integrated spaces. 
      - It was also recently repainted, so it looks brand new.
      - 1 bedroom. Originally, it had two, but one was converted into a home office.
      - 1 integrated kitchen and living room. The kitchen is very elegant, with a central eating wood table,
        with 60s-style chairs. The appliances are in gray and steel, and the cabinets are in white, the wood
        is light colored.
      - Has wood-like floors in all rooms, except the kitchen and bathroom, which are tiled.  
      - 2 bathrooms. Both with good taste porcelain and other decorative elements.
      - 1 laundry room. The washing machine is new and also doubles as a dryer.
      - Is already furnished with a bed, a sofa, a table, a desk, a chair, a washing machine, a refrigerator, 
        a stove, and a microwave.
      - It has a spacious shelf for books and other objects.
      - It is close to: a very convenient supermarket, a bakery, a gym, a bus stop, and a subway station. 
        It is also close to a great argentinian restaurant, and a pizzeria.
      - It is located at a main avenue, but the appartment is in the back of the building, so it is very quiet.
      - It is near of the best Medicine School in the country, so it is a good place for a medical student.  
    """
    
    # Create discussion with additional context
    discussion = ApartmentAdDiscussion(apartment_desc)
    discussion.add_context("target_audience", "medical students")
    discussion.add_context("location", "main avenue")
    discussion.add_context("nearby_amenities", [
        "supermarket", "bakery", "gym", "bus stop", "subway",
        "restaurant", "pizzeria", "medical school"
    ])
    
    # Run discussion and save results
    results = discussion.run_discussion()
    discussion.save_results(
        results,
        "data/extractions/appartment_rent_ad.extraction.json"
    )

if __name__ == "__main__":
    main()
