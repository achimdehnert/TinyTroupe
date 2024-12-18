#!/usr/bin/env python
# coding: utf-8

# # Online Advertisement Evaluation for TVs
# 
# Let's evaluate some online ads options to pick the best one.

# In[ ]:


import json
import sys
sys.path.append('..')

# import tinytroupe  # Removed legacy import
from group_cases.src.core.characters import TinyPerson
from tinytroupe.examples import create_lisa_the_data_scientist, create_oscar_the_architect
from group_cases.src.core.characters import TinyPersonFactory

from group_cases.src.utils.result_processor import ResultsExtractor


# ## Judging the best ad
# 
# Consider the following ads, obtained from real Bing queries.

# In[2]:


# User search query: "55 inches tv"

tv_ad_1 =\
"""
The Best TV Of Tomorrow - LG 4K Ultra HD TV
https://www.lg.com/tv/oled
AdThe Leading Name in Cinematic Picture. Upgrade Your TV to 4K OLED And See The Difference. It's Not Just OLED, It's LG OLED. Exclusive a9 Processor, Bringing Cinematic Picture Home.

Infinite Contrast · Self-Lighting OLED · Dolby Vision™ IQ · ThinQ AI w/ Magic Remote

Free Wall Mounting Deal
LG G2 97" OLED evo TV
Free TV Stand w/ Purchase
World's No.1 OLED TV
"""

tv_ad_2 =\
"""
The Full Samsung TV Lineup - Neo QLED, OLED, 4K, 8K & More
https://www.samsung.com
AdFrom 4K To 8K, QLED To OLED, Lifestyle TVs & More, Your Perfect TV Is In Our Lineup. Experience Unrivaled Technology & Design In Our Ultra-Premium 8K & 4K TVs.

Discover Samsung Event · Real Depth Enhancer · Anti-Reflection · 48 mo 0% APR Financing

The 2023 OLED TV Is Here
Samsung Neo QLED 4K TVs
Samsung Financing
Ranked #1 By The ACSI®
"""

tv_ad_3 =\
"""
Wayfair 55 Inch Tv - Wayfair 55 Inch Tv Décor
Shop Now
https://www.wayfair.com/furniture/free-shipping
AdFree Shipping on Orders Over $35. Shop Furniture, Home Décor, Cookware & More! Free Shipping on All Orders Over $35. Shop 55 Inch Tv, Home Décor, Cookware & More!
"""


# Let's build a request for our agents to pick the best ad.

# In[3]:


eval_request_msg = \
f"""
Can you evaluate these Bing ads for me? Which one convices you more to buy their particular offering? Select **ONLY** one. Please explain your reasoning, based on your background and personality.

# AD 1
```
{tv_ad_1}
```

# AD 2
```
{tv_ad_2}
```

# AD 3
```
{tv_ad_3}
```
"""

print(eval_request_msg)


# Let's also have a reason for them to require a new TV.

# In[4]:


situation = "Your TV broke and you need a new one. You search for a new TV on Bing."


# ### Try with standard agents
# 
# To begin with, let's pick a pre-defined agent and ask him or her to perform the evaluations. To make it easier to change the chosen agent, we assign it to a variable first.

# In[5]:


TinyPerson.all_agents


# In[6]:


lisa = create_lisa_the_data_scientist()


# In[7]:


lisa.change_context(situation)


# In[8]:


lisa.listen_and_act(eval_request_msg)


# Let's extract from the agent's interaction the best ad chosen. In this manner, we can easily process results later.

# In[ ]:


extractor = ResultsExtractor()

extraction_objective="Find the ad the agent chose. Extract the Ad number and title."

res = extractor.extract_results_from_agent(lisa, 
                          extraction_objective=extraction_objective,
                          situation=situation,
                          fields=["ad_number", "ad_title"],
                          verbose=True)

res


# We can then easily get the ad number and title from the results:

# In[10]:


f"{res['ad_number']}: {res['ad_title']}"


# ### Try with agents generated on the fly too
# 
# We don't really need to spend a lot of time customizing agents. We can create them on the fly from simple descriptions.

# In[11]:


TinyPerson.all_agents


# In[12]:


factory = TinyPersonFactory("Generates people with a broad range of personalities, backgrounds and socioeconomic status.")


# In[13]:


TinyPerson.all_agents


# In[14]:


factory.generated_minibios


# In[15]:


people = [factory.generate_person("A Brazilian person that is a doctor, like pets and the nature and love heavy metal."),
          factory.generate_person("A graphic designer who is an art and travel lover. Also uses TV as a computer monitor for work."),
          factory.generate_person("A wealthy banker who loves to show his money to others. Only uses the top and most expensive brands."),
          factory.generate_person("A poor grad student who is always looking for a bargain. Needs loans for everything.")]


# In[16]:


TinyPerson.all_agents


# In[17]:


factory.generated_minibios


# In[18]:


for person in people:
    person.listen_and_act(eval_request_msg)
    print("---------------------")


# In[ ]:


extractor = ResultsExtractor()
extraction_objective="Find the ad the agent chose. Extract the Ad number and title. Extract only ONE result."

choices =[]

for person in people:
    res = extractor.extract_results_from_agent(person,
                                    extraction_objective=extraction_objective,
                                    situation=situation,
                                    fields=["ad_number", "ad_title"],
                                    fields_hints={"ad_number": "Must be an integer, not a string."},
                                    verbose=True)

    choices.append(res)


# In[20]:


choices


# In[24]:


votes = {}
for choice in choices:
    print(f"{choice['ad_number']}: {choice['ad_title']}")

    ad_number = choice['ad_number']
    if ad_number not in votes:
        votes[ad_number] = 0
    votes[ad_number] += 1


# In[25]:


votes


# Finally, we pick the winner ad.

# In[26]:


# picks the most voted ad
winner = max(votes, key=votes.get)
winner

