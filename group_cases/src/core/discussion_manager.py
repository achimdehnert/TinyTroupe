"""
Discussion manager module for handling discussion flow and agent interactions.
"""
from typing import Dict, List, Any, Optional
import json
from tinytroupe.agent import TinyPerson as Agent
from tinytroupe.environment import TinyWorld
from .agent_group import AgentGroup
from .prompt import Prompt
from ..utils.result_processor import format_results
from .base_discussion import BaseDiscussion, DiscussionType

class DiscussionManager:
    """Manages the flow of discussions and agent interactions."""
    
    def __init__(self, discussion: BaseDiscussion):
        """
        Initialize discussion manager.
        
        Args:
            discussion: BaseDiscussion instance to manage
        """
        self.discussion = discussion
        self.agents: List[Agent] = []
        self.agent_group: Optional[AgentGroup] = None
        self.discussion_history = []
        self.world = TinyWorld(name=discussion.name)
        
    def setup_agents(self, roles: List[Dict[str, str]]) -> None:
        """
        Setup agents for the discussion using TinyTroupe.
        
        Args:
            roles: List of role definitions for agents
        """
        for role in roles:
            # Create TinyTroupe agent with role and personality
            config = self._generate_personality(role)
            agent = Agent(name=config["name"])
            
            # Configure agent
            agent.define("traits", config["traits"])
            agent.define("role", config["role"])
            
            self.agents.append(agent)
            self.world.add_agent(agent)
            
        # Create agent group for collaboration
        self.agent_group = AgentGroup(
            name=self.discussion.name,
            agents=self.agents
        )
        
    def _generate_personality(self, role: Dict[str, str]) -> Dict[str, str]:
        """
        Generate a personality configuration for an agent.
        
        Args:
            role: Role definition for the agent
            
        Returns:
            Dict containing the agent's personality configuration
        """
        return {
            "name": role.get("name", "Agent"),
            "role": role.get("description", ""),
            "traits": role.get("traits", [])
        }
        
    def _create_step_prompt(self, context: Dict[str, Any]) -> str:
        """
        Create a prompt for a discussion step.
        
        Args:
            context: Context for the step prompt
            
        Returns:
            Formatted prompt string
        """
        template = """
You are participating in a {discussion_type} discussion about {product}.

Current Context:
{context}

Task:
{task}

Previous Discussion:
{previous_discussion}

Your role is to {role}. Please provide your thoughts and suggestions based on your role and expertise.
"""
        prompt = Prompt(template=template)
        prompt.add_variable("discussion_type", self.discussion.discussion_type.value)
        prompt.add_variable("product", self.discussion.context.get("product", ""))
        prompt.add_variable("context", json.dumps(context.get("discussion_context", {}), indent=2))
        prompt.add_variable("task", context.get("phase", "").title())
        prompt.add_variable("previous_discussion", json.dumps(context.get("previous_results", []), indent=2))
        prompt.add_variable("role", context.get("role", "contribute to the discussion"))
        return prompt.format()
        
    def run_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single discussion step.
        
        Args:
            step: Step configuration with context and task
            
        Returns:
            Dict containing list of agent responses and summary
        """
        # Create step prompt
        step_prompt = self._create_step_prompt(step)
        
        # Run group discussion with fewer steps to avoid context length issues
        self.world.broadcast(step_prompt)
        try:
            responses = []
            for agent in self.agents:
                try:
                    agent_response = agent.act(return_actions=True)
                    if agent_response:
                        responses.append(agent_response[-1])  # Take only the last action
                except Exception as e:
                    print(f"Warning: Error during agent {agent.name} response: {str(e)}")
                    continue
        except Exception as e:
            print(f"Warning: Error during discussion step: {str(e)}")
            responses = []
        
        # Process and format responses
        formatted_responses = []
        for response in responses:
            if not isinstance(response, dict):
                continue
                
            agent = response.get("agent", "")
            action = response.get("action", {})
            
            if isinstance(action, dict):
                response_text = action.get("content", "")
            else:
                response_text = str(action)
                
            formatted_response = {
                "agent": agent,
                "response": response_text
            }
            formatted_responses.append(formatted_response)
        
        return {
            "responses": formatted_responses,
            "summary": "Discussion step completed"
        }
        
    def _get_coordination_prompt(self) -> str:
        """Get prompt for agent group coordination."""
        return f"""You are participating in a {self.discussion.discussion_type.value} about {self.discussion.name}.
        
        Context:
        {json.dumps(self.discussion.context, indent=2)}
        
        Guidelines:
        1. Stay focused on the discussion objective
        2. Build on others' contributions
        3. Provide constructive feedback
        4. Support claims with reasoning
        5. Maintain professional discourse
        
        Your responses should be clear, specific, and actionable."""
        
    def extract_results(self, raw_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract and format final results."""
        return format_results(raw_results, self.discussion.discussion_type.value)
