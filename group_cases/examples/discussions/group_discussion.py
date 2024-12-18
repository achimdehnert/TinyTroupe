#!/usr/bin/env python
# coding: utf-8

import json
import sys
import os
from typing import List, Dict, Any, Optional, Union
from enum import Enum
sys.path.append('..')

# import tinytroupe  # Removed legacy import
from group_cases.src.core.characters import TinyPerson
from group_cases.src.core.environment import TinyWorld, TinySocialNetwork
# Removed legacy wildcard import
from group_cases.src.utils.result_processor import ResultsExtractor, default_extractor, ResultsReducer
from group_cases.src.core.characters import TinyPersonFactory
from group_cases.src.utils.db_utils import DatabaseManager

class DiscussionType(Enum):
    FOCUS_GROUP = "focus_group"
    INTERVIEW = "interview"
    BRAINSTORMING = "brainstorming"
    EVALUATION = "evaluation"
    CUSTOM = "custom"

class GroupDiscussion:
    """A generalized class for managing various types of group discussions and interviews"""
    
    def __init__(self, 
                 discussion_name: str,
                 discussion_type: DiscussionType,
                 context: str = "",
                 agents: Optional[List[TinyPerson]] = None,
                 custom_factory: Optional[TinyPersonFactory] = None):
        """Initialize the discussion manager
        
        Args:
            discussion_name: Name of the discussion
            discussion_type: Type of discussion (focus group, interview, etc.)
            context: Context or background information for agent generation
            agents: List of predefined agents. If None, uses default agents or generates them
            custom_factory: Optional factory for generating custom agents
        """
        self.discussion_name = discussion_name
        self.discussion_type = discussion_type
        self.context = context
        self.db_manager = DatabaseManager()
        
        # Initialize agents based on discussion type and inputs
        if agents:
            self.agents = agents
        elif custom_factory:
            self.agents = self._generate_custom_agents(custom_factory)
        else:
            self.agents = self._get_default_agents()
            
        # Initialize the discussion world
        self.world = TinyWorld(discussion_name, self.agents)
        
        # Initialize discussion parameters
        self.situation = ""
        self.additional_context = {}
        self.extraction_config = {
            "objective": "",
            "fields": None,
            "rapporteur_name": None
        }
        
    def _generate_custom_agents(self, factory: TinyPersonFactory) -> List[TinyPerson]:
        """Generate custom agents using the provided factory"""
        # Override this in subclasses for specific agent generation logic
        return []
        
    def _get_default_agents(self) -> List[TinyPerson]:
        """Get default agents based on discussion type"""
        if self.discussion_type == DiscussionType.INTERVIEW:
            return [create_lisa_the_data_scientist()]  # Single interviewer
        else:
            return [
                create_lisa_the_data_scientist(),
                create_oscar_the_architect(),
                create_marcos_the_physician()
            ]
            
    def set_situation(self, situation: str):
        """Set the situation description"""
        self.situation = situation
        
    def add_context(self, key: str, value: Any):
        """Add additional context information"""
        self.additional_context[key] = value
        
    def configure_extraction(self, 
                           objective: str,
                           fields: Optional[List[str]] = None,
                           rapporteur_name: Optional[str] = None):
        """Configure how results should be extracted"""
        self.extraction_config.update({
            "objective": objective,
            "fields": fields,
            "rapporteur_name": rapporteur_name
        })
        
    def prepare_metadata(self) -> dict:
        """Prepare metadata for database storage"""
        metadata = {
            "discussion_type": self.discussion_type.value,
            "discussion_name": self.discussion_name,
            "context": self.context,
            **self.additional_context
        }
        return metadata
        
    def run_discussion(self, 
                      num_steps: int = 3,
                      reduce_results: bool = False) -> Dict[str, Any]:
        """Run the discussion and extract results
        
        Args:
            num_steps: Number of discussion steps
            reduce_results: Whether to reduce results from multiple agents
            
        Returns:
            Dictionary containing extracted results
        """
        # Broadcast situation if set
        if self.situation:
            self.world.broadcast(self.situation)
            
        # Run the discussion
        self.world.run(num_steps)
        
        # Extract results based on configuration
        if self.extraction_config["rapporteur_name"]:
            rapporteur = self.world.get_agent_by_name(self.extraction_config["rapporteur_name"])
            extractor = ResultsExtractor()
            extraction_result = extractor.extract_results_from_agent(
                rapporteur,
                extraction_objective=self.extraction_config["objective"],
                situation=self.situation
            )
        else:
            extraction_result = default_extractor.extract_results_from_world(
                self.world,
                extraction_objective=self.extraction_config["objective"],
                fields=self.extraction_config["fields"],
                verbose=True
            )
            
        # Reduce results if requested
        if reduce_results:
            reducer = ResultsReducer()
            extraction_result = reducer.reduce_results([extraction_result])
            
        return extraction_result
    
    def save_results(self, results: Dict[str, Any], output_file: str):
        """Save results to file and database"""
        # Save to file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
            
        # Save to databases with metadata
        metadata = self.prepare_metadata()
        self.db_manager.store_data(results, metadata)
        
        print(f"Results saved to {output_file} and stored in databases")
        
class ApartmentAdDiscussion(GroupDiscussion):
    """Specialized discussion for creating apartment advertisements"""
    
    def __init__(self, apartment_description: str):
        super().__init__(
            "Apartment Ad Discussion",
            DiscussionType.FOCUS_GROUP,
            "Creating an effective apartment rental advertisement"
        )
        
        self.add_context("property_type", "apartment")
        self.set_situation(
        """
        This is a focus group dedicated to finding the best way to advertise an apartment for rent.
        Everyone in the group is a friend to the person who is renting the apartment.
        The objective is to find the best way to advertise the apartment to find a good tenant.
        """)
        
        self.add_context("apartment_description", apartment_description)
        self.world.broadcast(apartment_description)
        
        self.configure_extraction(
            objective="Compose an advertisement copy based on the ideas given.",
            fields=["ad_copy"]
        )
        
class ProductBrainstormingDiscussion(GroupDiscussion):
    """Specialized discussion for product feature brainstorming"""
    
    def __init__(self, product_name: str, industry: str):
        super().__init__(
            f"{product_name} Feature Brainstorming",
            DiscussionType.BRAINSTORMING,
            f"Brainstorming innovative AI features for {product_name}"
        )
        
        self.add_context("product_name", product_name)
        self.add_context("industry", industry)
        
        self.set_situation(
        f"""
        We are brainstorming ideas for new features to add to {product_name}. The focus is on making
        {industry} professionals more productive by leveraging the latest AI technologies.
        Please avoid obvious ideas and focus on innovative solutions that could transform how people work.
        """)
        
        self.configure_extraction(
            objective="Summarize the ideas that the group came up with, explaining each idea as an item of a list. " \
                     "Describe in details the benefits and drawbacks of each.",
            rapporteur_name="Lisa"
        )
        
class CustomerInterviewDiscussion(GroupDiscussion):
    """Specialized discussion for customer interviews"""
    
    def __init__(self, company_context: str, customer_profile: str):
        super().__init__(
            "Customer Interview",
            DiscussionType.INTERVIEW,
            company_context,
            custom_factory=TinyPersonFactory(company_context)
        )
        
        self._generate_customer(customer_profile)
        self.configure_extraction(
            objective="Summarize the key insights from the customer interview",
            fields=["pain_points", "needs", "suggestions"]
        )
        
    def _generate_customer(self, profile: str):
        """Generate a customer agent based on the profile"""
        customer = self.custom_factory.generate_person(profile)
        self.agents.append(customer)
        self.world = TinyWorld(self.discussion_name, self.agents)
        
class AdEvaluationDiscussion(GroupDiscussion):
    """Specialized discussion for evaluating advertisements"""
    
    def __init__(self, product_type: str, ads: List[str]):
        super().__init__(
            f"{product_type} Ad Evaluation",
            DiscussionType.EVALUATION,
            f"Evaluating advertisements for {product_type}"
        )
        
        self.add_context("product_type", product_type)
        self.add_context("num_ads", len(ads))
        
        # Format ads for discussion
        ads_text = "\n\n".join([f"Ad {i+1}:\n{ad}" for i, ad in enumerate(ads)])
        self.set_situation(
        f"""
        We are evaluating {len(ads)} different advertisements for {product_type}.
        Please analyze each ad and discuss its strengths and weaknesses.
        
        {ads_text}
        """)
        
        self.configure_extraction(
            objective="Evaluate each advertisement and recommend the best one",
            fields=["rankings", "analysis", "recommendation"]
        )

def main():
    # Example 1: Apartment Ad
    apartment_desc = """
    Modern 1-bedroom apartment, fully renovated with integrated spaces.
    Close to medical school, supermarket, and public transport.
    Furnished with new appliances and elegant design elements.
    """
    apt_discussion = ApartmentAdDiscussion(apartment_desc)
    apt_results = apt_discussion.run_discussion()
    apt_discussion.save_results(apt_results, "data/extractions/apartment_ad.json")
    
    # Example 2: Product Brainstorming
    product_discussion = ProductBrainstormingDiscussion("Microsoft Word", "office productivity")
    product_results = product_discussion.run_discussion(num_steps=4)
    product_discussion.save_results(product_results, "data/extractions/word_features.json")
    
    # Example 3: Customer Interview
    company_context = "Large bank facing fintech competition"
    customer_profile = "VP of Innovation with engineering background and MBA"
    interview = CustomerInterviewDiscussion(company_context, customer_profile)
    interview_results = interview.run_discussion(num_steps=5)
    interview.save_results(interview_results, "data/extractions/customer_interview.json")
    
    # Example 4: Ad Evaluation
    tv_ads = [
        "Premium 4K OLED TV with infinite contrast...",
        "Next-gen QLED display with quantum processing..."
    ]
    ad_eval = AdEvaluationDiscussion("Television", tv_ads)
    eval_results = ad_eval.run_discussion(reduce_results=True)
    ad_eval.save_results(eval_results, "data/extractions/tv_ad_evaluation.json")

if __name__ == "__main__":
    main()
