#!/usr/bin/env python
# coding: utf-8

import json
import sys
import os
sys.path.append('..')

from focus_group_manager import FocusGroupManager

class ApartmentAdCreator(FocusGroupManager):
    def __init__(self):
        super().__init__("Apartment Ad Focus Group")
        
        self.set_situation(
        """ 
        This is a focus group dedicated to finding the best way to advertise an appartment for rent.
        Everyone in the group is a friend to the person who is renting the appartment, called Paulo.
        The objective is to find the best way to advertise the appartment, so that Paulo can find a good tenant.
        """)

        self.apartment_description = \
        """	
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

        self.set_task(
        """
        Discuss the best way to advertise the appartment, so that Paulo can find a good tenant.
        """)

    def prepare_metadata(self) -> dict:
        """Prepare metadata for database storage"""
        return {
            "property_type": "apartment",
            "target_audience": "medical students",
            "location_features": [
                "near Medicine School",
                "near supermarket",
                "near public transport",
                "quiet location"
            ],
            "amenities": [
                "washing machine/dryer",
                "fully furnished",
                "home office",
                "integrated kitchen",
                "wood floors"
            ],
            "rooms": {
                "bedrooms": 1,
                "bathrooms": 2,
                "office": 1,
                "laundry": 1
            }
        }

    def run(self):
        """Run the apartment ad focus group"""
        # Broadcast apartment description
        self.focus_group.broadcast(self.apartment_description)
        
        # Run focus group and extract results
        extraction_result = self.run_focus_group(
            num_steps=3,
            extraction_objective="Compose an advertisement copy based on the ideas given.",
            fields=["ad_copy"]
        )
        
        # Save results
        self.save_results(
            extraction_result,
            "data/extractions/appartment_rent_ad.extraction.json"
        )

def main():
    creator = ApartmentAdCreator()
    creator.run()

if __name__ == "__main__":
    main()
