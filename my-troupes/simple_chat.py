#!/usr/bin/env python
# coding: utf-8

# # Simple Chat
# 
# A simple demonstration of two agents talking to each other.

# In[5]:


import json
import sys
sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork
from tinytroupe.examples import *


# In[2]:


lisa = create_lisa_the_data_scientist()
oscar = create_oscar_the_architect()


# In[3]:


world = TinyWorld("Chat Room", [lisa, oscar])
world.make_everyone_accessible()


# In[4]:


lisa.listen("Talk to Oscar to know more about him")
world.run(4)


# In[6]:


lisa.pp_current_interactions()


# In[7]:


oscar.pp_current_interactions()


# In[ ]:




