#!/usr/bin/env python
# coding: utf-8

# # Wordprocessor usage example
# 
# 

# In[ ]:


import json
import sys
import csv
sys.path.insert(0, '..') # ensures that the package is imported from the parent directory, not the Python installation


# import tinytroupe  # Removed legacy import
from tinytroupe.openai_utils import force_api_type
from group_cases.src.core.characters import TinyPersonFactory
from group_cases.src.core.characters import TinyPerson, TinyToolUse
from group_cases.src.core.environment import TinyWorld
from tinytroupe import control
from group_cases.src.utils.result_processor import ResultsExtractor, ResultsReducer
from tinytroupe.enrichment import TinyEnricher
from group_cases.src.utils.result_processor import ArtifactExporter
from tinytroupe.tools import TinyWordProcessor
from tinytroupe.story import TinyStory
# import tinytroupe  # Removed legacy import.utils as utils
from tinytroupe.examples import create_lisa_the_data_scientist, create_oscar_the_architect, create_marcos_the_physician


# In[2]:


data_export_folder = "../data/extractions/wordprocessor"


# In[ ]:


exporter = ArtifactExporter(base_output_folder=data_export_folder)
enricher = TinyEnricher()
tooluse_faculty = TinyToolUse(tools=[TinyWordProcessor(exporter=exporter, enricher=enricher)])


# In[5]:


lisa = create_lisa_the_data_scientist()


# In[6]:


lisa.add_mental_faculties([tooluse_faculty])


# In[8]:


lisa.listen_and_act("You have just been fired and need to find a new job. You decide to think about what you want in life and then write a resume.")


# In[9]:


lisa.listen_and_act("What did I just told you?")


# In[ ]:



