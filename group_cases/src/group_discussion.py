#!/usr/bin/env python
# coding: utf-8

import json
import sys
import os
from typing import List, Dict, Any, Optional, Union
from enum import Enum
sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork
from tinytroupe.examples import *
from tinytroupe.extraction import ResultsExtractor, default_extractor, ResultsReducer
from tinytroupe.factory import TinyPersonFactory
from db_utils import DatabaseManager

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
        agents = []
        
        # Create a unique instance of Lisa for each discussion
        if self.discussion_type == DiscussionType.INTERVIEW:
            lisa = create_lisa_the_data_scientist()
            lisa.name = f"Lisa_{self.discussion_name}"  # Make name unique
            agents = [lisa]
        else:
            # Create unique instances for each agent
            lisa = create_lisa_the_data_scientist()
            oscar = create_oscar_the_architect()
            marcos = create_marcos_the_physician()
            
            # Make names unique by appending discussion name
            lisa.name = f"Lisa_{self.discussion_name}"
            oscar.name = f"Oscar_{self.discussion_name}"
            marcos.name = f"Marcos_{self.discussion_name}"
            
            agents = [lisa, oscar, marcos]
        
        return agents
            
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

    def get_results(self) -> Dict[str, Any]:
        """Extract and return results from the discussion"""
        # Create an extractor
        extractor = ResultsExtractor()
        
        # Extract results based on configuration
        if self.extraction_config["rapporteur_name"]:
            rapporteur = next(
                (agent for agent in self.agents 
                 if agent.name == self.extraction_config["rapporteur_name"]),
                None
            )
            if rapporteur:
                results = extractor.extract_results_from_agent(
                    rapporteur,
                    extraction_objective=self.extraction_config["objective"],
                    fields=self.extraction_config["fields"]
                )
            else:
                # Fallback to world extraction if rapporteur not found
                results = extractor.extract_results_from_world(
                    self.world,
                    extraction_objective=self.extraction_config["objective"],
                    fields=self.extraction_config["fields"]
                )
        else:
            results = extractor.extract_results_from_world(
                self.world,
                extraction_objective=self.extraction_config["objective"],
                fields=self.extraction_config["fields"]
            )
        
        # If fields are specified, ensure they exist in results
        if results and self.extraction_config["fields"]:
            for field in self.extraction_config["fields"]:
                if field not in results:
                    results[field] = None
        
        return results or {}
    
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
        
        # Get results
        results = self.get_results()
        
        # Reduce results if requested
        if reduce_results:
            reducer = ResultsReducer()
            results = reducer.reduce_results([results])
            
        return results
    
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
        
        # Update rapporteur name to match the unique agent name
        self.configure_extraction(
            objective="Summarize the ideas that the group came up with, explaining each idea as an item of a list. " \
                     "Describe in details the benefits and drawbacks of each.",
            rapporteur_name=f"Lisa_{self.discussion_name}"
        )

class CustomerInterviewDiscussion(GroupDiscussion):
    """Specialized discussion for customer interviews"""
    
    def __init__(self, company_context: str, customer_profile: str):
        # Create a custom factory for generating agents
        factory = TinyPersonFactory(company_context)
        
        # Call parent class constructor with all required arguments
        super().__init__(
            discussion_name="Customer Interview",
            discussion_type=DiscussionType.INTERVIEW,
            context=company_context,
            custom_factory=factory
        )
        
        # Set up the interview situation
        self.set_situation(
            f"""
            This is a customer interview session. The interviewer will ask questions to understand
            the customer's needs, pain points, and suggestions.
            
            Customer Profile:
            {customer_profile}
            """
        )
        
        # Configure how to extract results
        self.configure_extraction(
            objective="Summarize the key insights from the customer interview",
            fields=["pain_points", "needs", "suggestions"]
        )

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
