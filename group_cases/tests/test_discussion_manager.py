"""
Unit tests for the discussion manager module.
"""
import unittest
from unittest.mock import Mock, patch
from group_cases.src.core.discussion_manager import DiscussionManager, Agent, AgentGroup
from group_cases.src.core.base_discussion import BaseDiscussion, DiscussionType
from group_cases.src.core.prompt import Prompt

class TestDiscussionManager(unittest.TestCase):
    """Test cases for DiscussionManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_discussion = Mock(spec=BaseDiscussion)
        self.mock_discussion.name = "Test Discussion"
        self.mock_discussion.discussion_type = DiscussionType.BRAINSTORMING
        self.mock_discussion.context = {}
        
        self.manager = DiscussionManager(self.mock_discussion)
        
    def test_initialization(self):
        """Test manager initialization."""
        self.assertEqual(self.manager.discussion, self.mock_discussion)
        self.assertEqual(len(self.manager.agents), 0)
        self.assertIsNone(self.manager.agent_group)
        
    @patch('group_cases.src.core.discussion_manager.Agent')
    @patch('group_cases.src.core.discussion_manager.AgentGroup')
    def test_setup_agents(self, mock_agent_group, mock_agent):
        """Test agent setup."""
        # Setup mock agents
        mock_agent.return_value = Mock()
        mock_agent_group.return_value = Mock()
        
        # Test roles
        roles = [
            {"name": "Moderator", "role": "Guide discussion"},
            {"name": "Observer", "role": "Take notes"}
        ]
        
        self.manager.setup_agents(roles)
        
        # Verify agents were created
        self.assertEqual(mock_agent.call_count, len(roles))
        self.assertEqual(len(self.manager.agents), len(roles))
        
        # Verify agent group was created
        mock_agent_group.assert_called_once()
        self.assertIsNotNone(self.manager.agent_group)
        
    @patch('group_cases.src.core.discussion_manager.AgentGroup')
    def test_run_step_without_setup(self, mock_agent_group):
        """Test running step without setup."""
        with self.assertRaises(RuntimeError):
            self.manager.run_step({})
            
    @patch('group_cases.src.core.discussion_manager.Agent')
    @patch('group_cases.src.core.discussion_manager.AgentGroup')
    def test_run_step(self, mock_agent_group, mock_agent):
        """Test running a discussion step."""
        # Setup mocks
        mock_agent.return_value = Mock()
        mock_group = Mock()
        mock_group.discuss.return_value = [
            Mock(
                agent_name="Agent1",
                content="Response1",
                metadata={"key": "value"}
            )
        ]
        mock_agent_group.return_value = mock_group
        
        # Setup agents
        self.manager.setup_agents([
            {"name": "Agent1", "role": "Role1"}
        ])
        
        # Run step
        result = self.manager.run_step({
            "phase": "test_phase",
            "previous_results": []
        })
        
        # Verify results
        self.assertEqual(result["phase"], "test_phase")
        self.assertEqual(len(result["responses"]), 1)
        self.assertEqual(result["responses"][0]["agent"], "Agent1")
        self.assertEqual(result["responses"][0]["response"], "Response1")
        
    def test_generate_personality(self):
        """Test personality generation."""
        # Test known role
        moderator_traits = self.manager._generate_personality({
            "name": "Moderator",
            "role": "Guide"
        })
        self.assertEqual(moderator_traits["assertiveness"], 0.8)
        self.assertEqual(moderator_traits["empathy"], 0.9)
        
        # Test unknown role
        default_traits = self.manager._generate_personality({
            "name": "Unknown",
            "role": "Something"
        })
        self.assertEqual(default_traits["adaptability"], 0.7)
        self.assertEqual(default_traits["engagement"], 0.8)
        
        role = {"name": "TestAgent", "role": "Test Role"}
        personality = self.manager._generate_personality(role)
        self.assertIsInstance(personality, dict)
        self.assertIn("name", personality)
        self.assertIn("role", personality)
        
    def test_create_step_prompt(self):
        """Test creating step prompt."""
        context = {
            "phase": "test_phase",
            "previous_results": [],
            "discussion_context": {"key": "value"}
        }
        
        prompt = self.manager._create_step_prompt(context)
        
        # Verify prompt structure
        self.assertIsInstance(prompt, Prompt)
        self.assertIn("test_phase", prompt.template)
        self.assertEqual(prompt.variables["phase"], "test_phase")
        self.assertEqual(prompt.variables["step"], 1)
        
if __name__ == '__main__':
    unittest.main()
