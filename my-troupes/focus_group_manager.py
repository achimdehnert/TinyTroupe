#!/usr/bin/env python
# coding: utf-8

import json
import sys
import os
from typing import List, Dict, Any, Optional
sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork
from tinytroupe.examples import *
from tinytroupe.extraction import ResultsExtractor, default_extractor
from db_utils import DatabaseManager

class FocusGroupManager:
    """Base class for managing focus group discussions and extractions"""
    
    def __init__(self, group_name: str, agents: List[TinyPerson] = None):
        """Initialize the focus group manager
        
        Args:
            group_name: Name of the focus group
            agents: List of TinyPerson agents. If None, uses default agents.
        """
        if agents is None:
            agents = [
                create_lisa_the_data_scientist(),
                create_oscar_the_architect(),
                create_marcos_the_physician()
            ]
        
        self.focus_group = TinyWorld(group_name, agents)
        self.situation = ""
        self.task = ""
        self.db_manager = DatabaseManager()
        
    def set_situation(self, situation: str):
        """Set the situation description for the focus group"""
        self.situation = situation
        
    def set_task(self, task: str):
        """Set the task for the focus group"""
        self.task = task
        
    def prepare_metadata(self) -> dict:
        """Prepare metadata for database storage. Override in child classes."""
        return {}
        
    def run_focus_group(self, num_steps: int = 3, extraction_objective: str = "", 
                       fields: List[str] = None, rapporteur_name: str = None) -> Dict[str, Any]:
        """Run the focus group discussion and extract results
        
        Args:
            num_steps: Number of discussion steps
            extraction_objective: Objective for the extraction
            fields: Specific fields to extract
            rapporteur_name: Name of the agent to use as rapporteur
            
        Returns:
            Dictionary containing extracted results
        """
        # Broadcast situation and task
        self.focus_group.broadcast(self.situation)
        self.focus_group.broadcast(self.task)
        
        # Run the discussion
        self.focus_group.run(num_steps)
        
        # Handle extraction
        if rapporteur_name:
            rapporteur = self.focus_group.get_agent_by_name(rapporteur_name)
            extractor = ResultsExtractor()
            extraction_result = extractor.extract_results_from_agent(
                rapporteur,
                extraction_objective=extraction_objective,
                situation=self.situation
            )
        else:
            extraction_result = default_extractor.extract_results_from_world(
                self.focus_group,
                extraction_objective=extraction_objective,
                fields=fields,
                verbose=True
            )
            
        return extraction_result
    
    def save_results(self, results: Dict[str, Any], output_file: str):
        """Save results to file and database
        
        Args:
            results: Dictionary containing results to save
            output_file: Path to output file
        """
        # Save to file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
            
        # Save to databases with metadata
        metadata = self.prepare_metadata()
        self.db_manager.store_data(results, metadata)
        
        print(f"Results saved to {output_file} and stored in databases")
