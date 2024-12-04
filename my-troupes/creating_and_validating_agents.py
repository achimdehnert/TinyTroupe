#!/usr/bin/env python
# coding: utf-8

"""
Creating and Validating Agents

This module demonstrates how to create and validate agents using TinyTroupe.
"""

import json
import sys
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.validation import TinyPersonValidator
from tinytroupe.extraction import default_extractor as extractor
from tinytroupe.extraction import ResultsReducer
import tinytroupe.control as control
import textwrap

# Define the banker specification
banker_spec = """
A vice-president of one of the largest brazillian banks. Has a degree in engineering and an MBA in finance. 
Is facing a lot of pressure from the board of directors to fight off the competition from the fintechs.    
"""

# Create the banker
banker_factory = TinyPersonFactory(banker_spec)
banker = banker_factory.generate_person()
banker.minibio()

# Define expectations for validation
banker_expectations = """
He/she is:
 - Wealthy
 - Very intelligent and ambitious
 - Has a lot of connections
 - Is in his 40s or 50s

Tastes:
  - Likes to travel to other countries
  - Either read books, collect art or play golf
  - Enjoy only the best, most expensive, wines and food
  - Dislikes communists, unions and the like

Other notable traits:
  - Has some stress issues, and might be a bit of a workaholic
  - Deep knowledge of finance, economics and financial technology
  - Is a bit of a snob
  - Might pretend to be a hard-core woke, but in reality that's just a facade to climb the corporate ladder  
"""

# Validate the banker against expectations
banker_score, banker_justification = TinyPersonValidator.validate_person(
    banker, 
    expectations=banker_expectations, 
    include_agent_spec=False, 
    max_content_length=None
)

print(f"Banker validation score: {banker_score}")
print("\nValidation justification:")
print(textwrap.fill(banker_justification, width=100))

# Define the busy knowledge worker specification
bkw_spec = """
A typical knowledge worker in a large corporation grinding his way into upper middle class.
"""

# Create the busy knowledge worker
bkw_factory = TinyPersonFactory(bkw_spec)
busy_knowledge_worker = bkw_factory.generate_person()
busy_knowledge_worker.minibio()

# Define expectations for validation
bkw_expectations = """
Some characteristics of this person:
  - Very busy
  - Likes to have lunch with colleagues
  - To travel during vacations
  - Is married and worrying about the cost of living, particularly regarding his/her children
  - Has some stress issues, and potentially some psychiatric problems
  - Went to college and has a degree in some technical field
  - Has some very specific skills
  - Does not have a wide range of interests, being more focused on his/her career, family and very few hobbies if any
"""

# Validate the busy knowledge worker against expectations
score, justification = TinyPersonValidator.validate_person(
    busy_knowledge_worker, 
    expectations=bkw_expectations, 
    include_agent_spec=False, 
    max_content_length=None
)

print(f"\nBusy knowledge worker validation score: {score}")
print("\nValidation justification:")
print(textwrap.fill(justification, width=100))

# Validate the busy knowledge worker against the banker's expectations
wrong_expectations_score, wrong_expectations_justification = TinyPersonValidator.validate_person(
    busy_knowledge_worker, 
    expectations=banker_expectations, 
    include_agent_spec=False, 
    max_content_length=None
)

print(f"\nBusy knowledge worker validation score against banker's expectations: {wrong_expectations_score}")
print("\nValidation justification:")
print(textwrap.fill(wrong_expectations_justification, width=100))
