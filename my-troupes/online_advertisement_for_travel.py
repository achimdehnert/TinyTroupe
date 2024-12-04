#!/usr/bin/env python
# coding: utf-8

# # Online Advertisement Evaluation for Travel
# 
# Which travel ad work best?

# In[ ]:


import json
import sys
sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.examples import create_lisa_the_data_scientist, create_oscar_the_architect, create_marcos_the_physician
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.extraction import ResultsExtractor


# ## Judging the best ad
# 
# Consider the following ads, obtained from real Bing queries.

# In[2]:


# user search query: "europe travel package"

travel_ad_1 =\
"""
Tailor-Made Tours Of Europe - Nat'l Geographic Award Winner
https://www.kensingtontours.com/private-tours/europe
AdPrivate Guides; Custom Trip Itineraries; 24/7 In-Country Support. Request A Custom Quote. Europe's Best Customized For You - Historic Cities, Scenic Natural Wonders & More.

Unbeatable Value · Easy Multi-Country · Expert Safari Planners · Top Lodges

Bulgari & Romania
Explore Europe Off The Beaten Track
Exceptional Journey In The Balkans
Munich, Salzburg, Vienna
Discover Extraordinary Landscapes
Explore Castles & Royal Palaces
Budapest, Vienna, Prague
Tread Cobblestone Laneways
Bask In The Elegant Architecture
30,000+ Delighted Clients
Customers Love Kensington Tours
With A Trust Score Of 9.8 Out Of 10
Expert Planners
Our Experts Know The Must-Sees,
Hidden Gems & Everything In Between
Free Custom Quotes
Your Itinerary Is Tailored For You
By Skilled Destination Experts
See more at kensingtontours.com
"""

travel_ad_2 =\
"""
Europe all-inclusive Packages - Europe Vacation Packages
https://www.exoticca.com/europe/tours

AdDiscover our inspiring Europe tour packages from the US: Capitals, Beaches and much more. Enjoy our most exclusive experiences in Europe with English guides and Premium hotels

100% Online Security · +50000 Happy Customers · Flights + Hotels + Tours

Types: Lodge, Resort & Spa, Guest House, Luxury Hotel, Tented Lodge
"""

travel_ad_3 =\
"""
Travel Packages - Great Vacation Deals
https://www.travelocity.com/travel/packages
AdHuge Savings When You Book Flight and Hotel Together. Book Now and Save! Save When You Book Your Flight & Hotel Together At Travelocity.

Get 24-Hour Support · 3 Million Guest Reviews · 240,000+ Hotels Worldwide

Types: Cheap Hotels, Luxury Hotels, Romantic Hotels, Pet Friendly Hotels
Cars
Things to Do
Discover
All-Inclusive Resorts
Book Together & Save
Find A Hotel
Nat Geo Expeditions® - Trips to Europe
https://www.nationalgeographic.com/expeditions/europe
AdTravel Beyond Your Wildest Dreams. See the World Close-Up with Nat Geo Experts. Join Us for An Unforgettable Expedition! Discover the Nat Geo Difference.

People & Culture · Wildlife Encounters · Photography Trips · Hiking Trips

Find The Trip For You
Request a Free Catalog
Special Offers
Discover the Difference
"""

travel_ad_4 =\
"""
Europe Luxury Private Tours
https://www.kensingtontours.com
Kensington Tours - Private Guides, Custom Itineraries, Hand Picked Hotels & 24/7 Support
"""


# In[3]:


eval_request_msg = \
f"""
Can you evaluate these Bing ads for me? Which one convices you more to buy their particular offering? Select **ONLY** one. Please explain your reasoning, based on your background and personality.

# AD 1
```
{travel_ad_1}
```

# AD 2
```
{travel_ad_2}
```

# AD 3
```
{travel_ad_3}
```

# AD 4
```
{travel_ad_4}
```

"""

print(eval_request_msg)


# In[4]:


situation = "You decided you want to visit Europe and you are planning your next vacations. You start by searching for good deals as well as good ideas."


# In[5]:


extraction_objective="Find the ad the agent chose. Extract the Ad number, title and justification for the choice. Extract only ONE choice."


# ### Try with example agents
# 
# What our existing agents say?

# In[6]:


people = [create_lisa_the_data_scientist(), create_marcos_the_physician(), create_oscar_the_architect()]

for person in people:
    person.change_context(situation)
    person.listen_and_act(eval_request_msg)
    


# We can extract the result from each individual agent.

# In[ ]:


extractor = ResultsExtractor()
choices = []

for person in people:
    res = extractor.extract_results_from_agent(person,
                                    extraction_objective=extraction_objective,
                                    situation=situation,
                                    fields=["ad_id", "ad_title", "justification"])
    choices.append(res)


# In[8]:


print(choices)


# In[9]:


choices[0]


# ### Try with agents generated on the fly

# In[10]:


people = [TinyPersonFactory("Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.").generate_person(),
          TinyPersonFactory("Create a graphic designer who is an art and travel lover.").generate_person(),
          TinyPersonFactory("Create a wealthy banker who loves to show his money to others.").generate_person(),
          TinyPersonFactory("Create a poor grad student who loves history but has very little money to visit historical places.").generate_person()]


# In[11]:


for person in people:
    person.listen_and_act(eval_request_msg)
    print("---------------------")


# In[ ]:


extractor = ResultsExtractor()

choices =[]

for person in people:
    res = extractor.extract_results_from_agent(person,
                                    extraction_objective=extraction_objective,
                                    situation=situation,
                                    fields=["ad_id", "ad_title", "justification"])

    choices.append(res)
    print(res)
    print("---------------------")


# In[13]:


choices


# In[14]:


votes = {}
for choice in choices:
    print(f"{choice['ad_id']}: {choice['ad_title']}")
    if choice['ad_id'] not in votes:
        votes[choice['ad_id']] = 0
    votes[choice['ad_id']] += 1


# In[15]:


votes


# Finally, we pick the winning ad.

# In[16]:


# picks the most voted ad
winner = max(votes, key=votes.get)
winner

