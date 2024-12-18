"""
Environment classes for managing discussion worlds and social networks.
"""
from typing import List, Dict, Any
from .characters import TinyPerson

class TinyWorld:
    """A world environment for discussions"""
    
    def __init__(self, name: str, agents: List[TinyPerson]):
        self.name = name
        self.agents = agents
        self.social_network = TinySocialNetwork(agents)
        self.messages = []
        
    def broadcast(self, message: str):
        """Broadcast a message to all agents"""
        self.messages.append({"type": "broadcast", "content": message})
        for agent in self.agents:
            agent.receive_message(message)

class TinySocialNetwork:
    """Manages relationships between agents"""
    
    def __init__(self, agents: List[TinyPerson]):
        self.agents = agents
        self.relationships = {}
        self._initialize_relationships()
        
    def _initialize_relationships(self):
        """Initialize basic relationships between all agents"""
        for agent1 in self.agents:
            self.relationships[agent1.name] = {}
            for agent2 in self.agents:
                if agent1 != agent2:
                    self.relationships[agent1.name][agent2.name] = {
                        "trust": 0.5,
                        "familiarity": 0.0
                    }
    
    def update_relationship(self, agent1: str, agent2: str, 
                          trust_delta: float = 0.0, 
                          familiarity_delta: float = 0.1):
        """Update relationship metrics between two agents"""
        if agent1 in self.relationships and agent2 in self.relationships[agent1]:
            self.relationships[agent1][agent2]["trust"] += trust_delta
            self.relationships[agent1][agent2]["familiarity"] += familiarity_delta
            
            # Ensure values stay in valid range
            self.relationships[agent1][agent2]["trust"] = max(0.0, min(1.0, 
                self.relationships[agent1][agent2]["trust"]))
            self.relationships[agent1][agent2]["familiarity"] = max(0.0, min(1.0,
                self.relationships[agent1][agent2]["familiarity"]))
