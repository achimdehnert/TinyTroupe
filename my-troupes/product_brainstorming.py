#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.append('..')

from focus_group_manager import FocusGroupManager

class ProductBrainstorming(FocusGroupManager):
    def __init__(self, product_name: str, industry: str):
        super().__init__(f"{product_name} Brainstorming Group")
        self.product_name = product_name
        self.industry = industry
        
        self.set_situation(
        f"""
        We are brainstorming ideas for new features to add to {product_name}. The focus is on making
        {industry} professionals more productive by leveraging the latest AI technologies.
        Please avoid obvious ideas and focus on innovative solutions that could transform how people work.
        """)
        
        self.set_task(
        """
        Please start the discussion by proposing and discussing potential AI feature ideas.
        Consider both the technical feasibility and the practical benefits for users.
        """)
        
    def prepare_metadata(self) -> dict:
        """Prepare metadata for database storage"""
        return {
            "product_name": self.product_name,
            "industry": self.industry,
            "brainstorm_type": "feature_ideas",
            "focus": "AI integration",
            "target_audience": f"{self.industry} professionals"
        }
        
    def run(self):
        """Run the product brainstorming session"""
        # Run focus group with Lisa as rapporteur
        extraction_result = self.run_focus_group(
            num_steps=4,
            extraction_objective="Summarize the ideas that the group came up with, explaining each idea as an item of a list. " \
                               "Describe in details the benefits and drawbacks of each.",
            rapporteur_name="Lisa"
        )
        
        # Save results
        self.save_results(
            extraction_result,
            f"data/extractions/{self.product_name.lower()}_brainstorming.extraction.json"
        )

def main():
    brainstorming = ProductBrainstorming("Microsoft Word", "office productivity")
    brainstorming.run()

if __name__ == "__main__":
    main()
