import unittest
from datetime import datetime
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from enhanced_group_memory.src.core.characters import Character, CharacterGroup
from enhanced_group_memory.src.core.discussion import GroupDiscussion, DiscussionType

class TestCharacterGroup(unittest.TestCase):
    def setUp(self):
        # Clear any existing environments and agents
        TinyWorld.clear_environments()
        TinyPerson.clear_agents()
        
        # Create test characters
        self.lisa = Character(
            name="Lisa_Test",
            age=28,
            occupation="Data Scientist",
            nationality="Canadian",
            interests=["Machine Learning", "Data Visualization"],
            personality=["Analytical", "Creative"]
        )
        self.oscar = Character(
            name="Oscar_Test",
            age=35,
            occupation="Architect",
            nationality="Spanish",
            interests=["Urban Design", "Sustainable Architecture"],
            personality=["Creative", "Detail-oriented"]
        )
        
    def test_character_group_initialization(self):
        # Test that character group creates a unique environment
        group1 = CharacterGroup([self.lisa])
        self.assertEqual(group1.world.name, "Discussion Room 1")
        
        group2 = CharacterGroup([self.oscar])
        self.assertEqual(group2.world.name, "Discussion Room 2")
        
        # Verify environments are tracked correctly
        self.assertIn(group1.world.name, TinyWorld.all_environments)
        self.assertIn(group2.world.name, TinyWorld.all_environments)
    
    def test_discussion_start(self):
        group = CharacterGroup([self.lisa, self.oscar])
        
        # Start a discussion
        discussion = group.start_discussion(
            topic="AI in Architecture",
            initial_prompt="How can AI enhance architectural design?"
        )
        
        # Verify discussion was created correctly
        self.assertIsInstance(discussion, GroupDiscussion)
        self.assertEqual(discussion.discussion_type, DiscussionType.CUSTOM)
        
        # Verify initial message was added
        self.assertTrue(len(discussion.chat_interface.messages) > 0)
        first_msg = discussion.chat_interface.messages[0]
        self.assertEqual(first_msg.sender, "System")
        self.assertEqual(first_msg.content, "How can AI enhance architectural design?")
    
    def test_character_response(self):
        group = CharacterGroup([self.lisa])
        discussion = group.start_discussion(
            topic="Data Science",
            initial_prompt="What are the key trends in data science?"
        )
        
        # Verify that we got the initial response
        self.assertTrue(len(discussion.chat_interface.messages) > 1)
        first_response = discussion.chat_interface.messages[1]
        self.assertEqual(first_response.sender, self.lisa.name)
        self.assertIsInstance(first_response.content, str)
        self.assertTrue(len(first_response.content) > 0)

if __name__ == '__main__':
    unittest.main()
