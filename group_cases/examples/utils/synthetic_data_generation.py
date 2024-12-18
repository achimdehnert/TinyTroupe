#!/usr/bin/env python
# coding: utf-8

# # Synthetic Data Generation
# 

# In[ ]:


import json
import sys
import csv
sys.path.append('..')


# import tinytroupe  # Removed legacy import
from group_cases.src.core.characters import TinyPerson
from group_cases.src.core.environment import TinyWorld, TinySocialNetwork
from group_cases.src.core.characters import TinyPersonFactory
from group_cases.src.utils.result_processor import default_extractor as extractor
from group_cases.src.utils.result_processor import ResultsReducer
# import tinytroupe  # Removed legacy import.control as control


# Let's create the specific types of agents we need to collect data.

# In[2]:


factory = TinyPersonFactory("A random knowledge worker in a company providing marketing services.")


# In[3]:


people = []
for i in range(2):
    person = factory.generate_person(temperature=1.6)
    print(person.minibio())
    people.append(person)

len(people)


# In[4]:


company = TinyWorld("Some Corp Inc.", people)


# In[5]:


company.make_everyone_accessible()


# In[6]:


company.broadcast("Message each other to get work done.")


# In[7]:


company.run(2)


# In[ ]:





# We can now extract the conversations, which form the synthetic corpus we wanted.

# In[8]:


people[0].pp_current_interactions()


# In[ ]:


reducer = ResultsReducer()

def aux_extract_content(focus_agent: TinyPerson, source_agent:TinyPerson, target_agent:TinyPerson, kind:str, event: str, content: str, timestamp:str):

    if event == "TALK":
        author = focus_agent.name
    elif event == "CONVERSATION":
        if source_agent is None:
            author = "USER"
        else:
            author = source_agent.name
    else:
        raise ValueError(f"Unknown event: {event}")
    
    
    entry = (author, content)
    print(entry)
    return entry
    


reducer.add_reduction_rule("TALK", aux_extract_content)
reducer.add_reduction_rule("CONVERSATION", aux_extract_content)


# Finally, we obtain the dataframe with the data and save it to a `.csv`, for later use in other applications.

# In[10]:


df = reducer.reduce_agent_to_dataframe(people[0], column_names=["author", "content"])
df


# In[11]:


df.to_csv("../data/extractions/synthetic_data_generation.out.csv", index=False)

