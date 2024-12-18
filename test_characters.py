from enhanced_group_memory.src.core.characters import Character, CharacterGroup
from enhanced_group_memory.src.core.discussion import GroupDiscussion, MessageType, DiscussionType
from tinytroupe.agent import TinyPerson, EpisodicMemory
from tinytroupe.memory import EnhancedSemanticMemory

def create_test_character():
    """Create a test character."""
    # Create TinyPerson with memory first
    tiny_person = TinyPerson(
        name="Test_Character",
        episodic_memory=EpisodicMemory(),
        semantic_memory=EnhancedSemanticMemory()
    )
    
    # Create character with TinyPerson
    return Character(
        name="Test Character",
        age=30,
        occupation="Senior Data Scientist",
        nationality="American",
        interests=["machine learning", "data analytics", "statistics"],
        personality=["analytical", "thoughtful", "detail-oriented"],
        tiny_person=tiny_person
    )

def test_character_response():
    """Test character response generation."""
    # Create character
    character = create_test_character()
    
    # Create group with single character
    group = CharacterGroup([character])
    
    # Create discussion
    discussion = GroupDiscussion(
        discussion_name="Test Discussion",
        discussion_type=DiscussionType.CUSTOM,
        context="Testing character responses"
    )
    
    # Add test prompt
    test_prompt = "What are your thoughts on machine learning applications in healthcare?"
    discussion.chat_interface.add_message(
        sender="System",
        content=test_prompt,
        msg_type=MessageType.SYSTEM
    )
    
    print("\nGenerating character response...")
    print("Character:", character.name)
    print("Prompt:", test_prompt)
    
    # Generate response
    response = group._generate_character_response(character, test_prompt, discussion)
    
    print("\nResponse:", response)
    print("Response type:", type(response))
    
    # Check character's memory
    print("\nCharacter's recent memory:")
    recent_memory = character.tiny_person.episodic_memory.retrieve_recent()
    for memory in recent_memory:
        print(f"Memory: {memory}")

if __name__ == "__main__":
    test_character_response()
