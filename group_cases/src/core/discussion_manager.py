"""
Discussion manager module for handling discussion flow and agent interactions.
"""
from typing import Dict, List, Any, Optional
import json
from tinytroupe import Agent, AgentGroup, Prompt
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
        
    def setup_agents(self, roles: List[Dict[str, str]]) -> None:
        """
        Setup agents for the discussion using TinyTroupe.
        
        Args:
            roles: List of role definitions for agents
        """
        for role in roles:
            # Create TinyTroupe agent with role and personality
            personality = self._generate_personality(role)
            agent = Agent(
                name=role["name"],
                role_description=role["role"],
                traits=personality
            )
            self.agents.append(agent)
            
        # Create agent group for collaboration
        self.agent_group = AgentGroup(
            agents=self.agents,
            coordination_prompt=self._get_coordination_prompt()
        )
            
    def _generate_personality(self, role: Dict[str, str]) -> Dict[str, float]:
        """Generate personality traits for TinyTroupe agent."""
        base_traits = {
            "Moderator": {"assertiveness": 0.8, "empathy": 0.9},
            "Evaluator": {"analytical": 0.9, "objectivity": 0.8},
            "Observer": {"attention": 0.9, "neutrality": 0.9},
            "Devil's Advocate": {"critical": 0.9, "constructive": 0.7}
        }
        
        role_name = role["name"]
        return base_traits.get(role_name, {"adaptability": 0.7, "engagement": 0.8})
        
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
        
    def run_step(self, step_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single discussion step using TinyTroupe agents.
        
        Args:
            step_config: Configuration for the step
            
        Returns:
            Results from the step
        """
        if not self.agent_group:
            raise RuntimeError("Agents not set up. Call setup_agents() first.")
            
        # Prepare step context
        context = {
            "phase": step_config.get("phase", "discussion"),
            "previous_results": step_config.get("previous_results", []),
            "discussion_context": self.discussion.context
        }
        
        # Create step-specific prompt
        step_prompt = self._create_step_prompt(context)
        
        # Run group discussion
        responses = self.agent_group.discuss(
            prompt=step_prompt,
            max_turns=3,  # Adjust based on discussion needs
            temperature=0.7
        )
        
        # Process and structure responses
        structured_responses = [
            {
                "agent": response.agent_name,
                "response": response.content,
                "metadata": response.metadata
            }
            for response in responses
        ]
            
        # Process step results
        step_result = {
            "phase": context["phase"],
            "responses": structured_responses,
            "summary": self._summarize_responses(structured_responses)
        }
        
        self.discussion_history.append(step_result)
        return step_result
        
    def _create_step_prompt(self, context: Dict[str, Any]) -> Prompt:
        """Create TinyTroupe prompt for the current step."""
        phase = context["phase"]
        previous = context["previous_results"]
        
        prompt_text = f"""Phase: {phase}
        
        Previous Discussion:
        {json.dumps(previous[-1] if previous else {}, indent=2)}
        
        Current Context:
        {json.dumps(context['discussion_context'], indent=2)}
        
        Please continue the discussion, focusing on the current phase objectives."""
        
        return Prompt(
            content=prompt_text,
            metadata={
                "phase": phase,
                "step": len(self.discussion_history) + 1
            }
        )
        
    def _summarize_responses(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize responses using a dedicated TinyTroupe agent."""
        if not self.agents:
            return {"error": "No agents available"}
            
        # Use the Observer agent if available, or the first agent
        summarizer = next(
            (a for a in self.agents if a.name == "Observer"),
            self.agents[0]
        )
        
        summary_prompt = f"""Please summarize the following discussion responses:
        
        {json.dumps(responses, indent=2)}
        
        Focus on:
        1. Key points and insights
        2. Areas of consensus
        3. Notable disagreements
        4. Action items or next steps"""
        
        summary_response = summarizer.generate(
            prompt=summary_prompt,
            temperature=0.3  # Lower temperature for more focused summary
        )
        
        return {
            "key_points": summary_response.key_points,
            "consensus": summary_response.consensus,
            "disagreements": summary_response.disagreements,
            "action_items": summary_response.action_items
        }
        
    def extract_results(self, raw_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract and format final results."""
        return format_results(raw_results, self.discussion.discussion_type.value)
