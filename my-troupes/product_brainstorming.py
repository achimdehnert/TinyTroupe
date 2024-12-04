#!/usr/bin/env python
# coding: utf-8

# # Product Brinstorming
# 
# Can we use TinyTroupe to brainstorm product ideas?

# In[1]:


import json
import sys
sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork
from tinytroupe.examples import *


# In[2]:


world = TinyWorld("Focus group", [create_lisa_the_data_scientist(), create_oscar_the_architect(), create_marcos_the_physician()])


# In[3]:


world.broadcast("""
             Folks, we need to brainstorm ideas for a new product. Your mission is to discuss potential AI feature ideas
             to add to Microsoft Word. In general, we want features that make you or your industry more productive,
             taking advantage of all the latest AI technologies. Also avoid obvious ideas, like summarization or
            translation.

             Please start the discussion now.
             """)


# In[4]:


world.run(4)


# In[6]:


rapporteur = world.get_agent_by_name("Lisa")


# In[7]:


rapporteur.listen_and_act("Can you please summarize the ideas that the group came up with?")


# In[ ]:


from tinytroupe.extraction import ResultsExtractor

extractor = ResultsExtractor()

extractor.extract_results_from_agent(rapporteur, 
                          extraction_objective="Summarize the the ideas that the group came up with, explaining each idea as an item of a list." \
                                               "Describe in details the benefits and drawbacks of each.", 
                          situation="A focus group to brainstorm ideas for a new product.")


# In[ ]:




