#!/usr/bin/env python
# coding: utf-8

# # Interview with customers
# 
# What if we could interview our precise target audience synthetically?
# 

# In[1]:


import json
import sys
sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.extraction import default_extractor as extractor
from tinytroupe.extraction import ResultsReducer
import tinytroupe.control as control


# Let's create the specific types of agents we need to collect data.

# In[2]:


factory = TinyPersonFactory("One of the largest banks in Brazil, full of bureaucracy and legacy systems.")

customer = factory.generate_person(
    """
    The vice-president of one product innovation. Has a degree in engineering and a MBA in finance. 
    Is facing a lot of pressure from the board of directors to fight off the competition from the fintechs.    
    """
)


# In[3]:


customer.minibio()


# We can now perform the interview.

# In[4]:


customer.think("I am now talking to a business and technology consultant to help me with my professional problems.")


# In[5]:


customer.listen_and_act("What would you say are your main problems today? Please be as specific as possible.", 
                        max_content_length=3000)


# In[6]:


customer.listen_and_act("Can you elaborate on the fintechs?", max_content_length=3000)


# In[7]:


customer.listen_and_act("If you could improve in one of these aspects to better compete, what would that be?", max_content_length=3000)


# In[8]:


customer.listen_and_act("Please give more detail about that, so that we can think about a project to pursue this direction.", 
                        max_content_length=3000)


# In[ ]:




