"""
Agent group module for managing collections of agents.
"""
from typing import List, Optional
from tinytroupe.agent import TinyPerson as Agent

class AgentGroup:
    """A group of agents that can interact with each other."""
    
    def __init__(self, name: str, agents: Optional[List[Agent]] = None):
        """
        Initialize agent group.
        
        Args:
            name (str): Name of the group
            agents (List[Agent], optional): List of agents in the group. Defaults to None.
        """
        self.name = name
        self.agents = agents or []
        
        # Make all agents accessible to each other
        for agent in self.agents:
            for other_agent in self.agents:
                if agent != other_agent:
                    agent.make_agent_accessible(other_agent)
                    
    def add_agent(self, agent: Agent) -> None:
        """
        Add an agent to the group.
        
        Args:
            agent (Agent): Agent to add
        """
        if agent not in self.agents:
            self.agents.append(agent)
            # Make the agent accessible to all other agents in the group
            for other_agent in self.agents:
                if other_agent != agent:
                    other_agent.make_agent_accessible(agent)
                    agent.make_agent_accessible(other_agent)
                    
    def remove_agent(self, agent: Agent) -> None:
        """
        Remove an agent from the group.
        
        Args:
            agent (Agent): Agent to remove
        """
        if agent in self.agents:
            self.agents.remove(agent)
            # Make the agent inaccessible to all other agents in the group
            for other_agent in self.agents:
                if other_agent != agent:
                    other_agent.make_agent_inaccessible(agent)
                    agent.make_agent_inaccessible(other_agent)
                    
    def get_agents(self) -> List[Agent]:
        """
        Get all agents in the group.
        
        Returns:
            List[Agent]: List of agents in the group
        """
        return self.agents
        
    def __len__(self) -> int:
        """
        Get number of agents in the group.
        
        Returns:
            int: Number of agents
        """
        return len(self.agents)
