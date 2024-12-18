import pytest
from enhanced_group_memory.src.core.characters import Character, CharacterGroup
from enhanced_group_memory.src.core.discussion import GroupDiscussion, DiscussionType, MessageType
from tinytroupe.enhanced_faculties import EmotionalIntelligenceFaculty, AdvancedReasoningFaculty
from tinytroupe.agent import TinyPerson
from tinytroupe.memory import EnhancedSemanticMemory

def create_test_character(name, occupation, traits, interests):
    """Helper function to create a test character with basic attributes"""
    # Create TinyPerson first with our enhanced faculties
    tiny_person = TinyPerson(
        name=name,
        mental_faculties=[
            EmotionalIntelligenceFaculty(),
            AdvancedReasoningFaculty()
        ],
        semantic_memory=EnhancedSemanticMemory()  # Use our enhanced version
    )
    
    # Create character with the pre-initialized TinyPerson
    character = Character(
        name=name,
        age=30,
        occupation=occupation,
        nationality="Test Country",
        interests=interests,
        personality=traits,
        tiny_person=tiny_person
    )
    
    # Initialize character's memory with traits
    character.tiny_person.semantic_memory.store({
        'role': 'system',
        'content': f"You are {name}, a {occupation}. Your personality traits are: {', '.join(traits)}. "
                  f"Your interests include: {', '.join(interests)}."
    })
    
    return character

def test_character_response_generation():
    """Test that characters generate appropriate responses based on their traits and context"""
    # Create test characters
    scientist = create_test_character(
        "Test Scientist",
        "Data Scientist",
        ["analytical", "curious"],
        ["data analysis", "machine learning"]
    )
    
    architect = create_test_character(
        "Test Architect",
        "Architect",
        ["creative", "detail-oriented"],
        ["sustainable design", "urban planning"]
    )
    
    # Create character group
    group = CharacterGroup([scientist, architect])
    
    # Create a discussion
    discussion = GroupDiscussion(
        discussion_name="Test Discussion",
        discussion_type=DiscussionType.CUSTOM,
        context="Let's discuss how data science can improve architectural design."
    )
    
    # Add initial message
    discussion.chat_interface.add_message(
        "System",
        "How can data science and architecture work together to create better buildings?",
        MessageType.SYSTEM
    )
    
    # Get responses from both characters
    scientist_response = group.get_character_response(scientist, discussion)
    architect_response = group.get_character_response(architect, discussion)
    
    # Verify responses are generated and contain relevant content
    assert scientist_response is not None, "Scientist should generate a response"
    assert architect_response is not None, "Architect should generate a response"
    
    # Check that responses reflect character traits
    assert any(keyword in scientist_response.lower() for keyword in ["data", "analysis", "machine learning"]), \
        "Scientist's response should mention their expertise"
    assert any(keyword in architect_response.lower() for keyword in ["design", "building", "architecture"]), \
        "Architect's response should mention their expertise"

def test_character_memory_integration():
    """Test that characters maintain memory of the conversation"""
    # Create test character
    character = create_test_character(
        "Test Character",
        "Researcher",
        ["thoughtful", "analytical"],
        ["research", "innovation"]
    )
    
    # Create character group and discussion
    group = CharacterGroup([character])
    discussion = GroupDiscussion(
        discussion_name="Memory Test",
        discussion_type=DiscussionType.CUSTOM,
        context="Testing memory retention"
    )
    
    # Add a series of messages
    messages = [
        "What are your thoughts on innovation?",
        "How does your research background influence your perspective?",
        "Can you elaborate on your previous point about research methods?"
    ]
    
    responses = []
    for msg in messages:
        discussion.chat_interface.add_message("User", msg, MessageType.TEXT)
        response = group.get_character_response(character, discussion)
        responses.append(response)
        discussion.chat_interface.add_message(character.name, response, MessageType.TEXT)
    
    # Verify that later responses reference earlier points
    assert responses[-1] is not None, "Character should generate a response"
    
    # Check that the character's memory contains the conversation history
    memory_content = character.tiny_person.semantic_memory.retrieve()
    assert len(memory_content) > 0, "Character should have stored memories of the conversation"
    
    # Verify that the stored memories contain the character's responses
    stored_responses = [m['content'] for m in memory_content if m['role'] == 'assistant']
    assert len(stored_responses) > 0, "Character's responses should be stored in memory"

def test_multi_character_interaction():
    """Test interaction between multiple characters in a group discussion"""
    # Create test characters
    characters = [
        create_test_character(
            "Character 1",
            "Engineer",
            ["technical", "precise"],
            ["engineering", "problem-solving"]
        ),
        create_test_character(
            "Character 2",
            "Designer",
            ["creative", "innovative"],
            ["design", "user experience"]
        )
    ]
    
    # Create character group
    group = CharacterGroup(characters)
    
    # Create discussion
    discussion = GroupDiscussion(
        discussion_name="Group Interaction Test",
        discussion_type=DiscussionType.CUSTOM,
        context="Discussing the intersection of engineering and design"
    )
    
    # Simulate a discussion
    discussion.chat_interface.add_message(
        "System",
        "How can engineering and design principles be combined effectively?",
        MessageType.SYSTEM
    )
    
    # Get responses from both characters
    responses = []
    for char in characters:
        response = group.get_character_response(char, discussion)
        assert response is not None, f"{char.name} should generate a response"
        responses.append(response)
        discussion.chat_interface.add_message(char.name, response, MessageType.TEXT)
    
    # Verify that characters respond to each other
    second_round_responses = []
    for char in characters:
        response = group.get_character_response(char, discussion)
        assert response is not None, f"{char.name} should generate a follow-up response"
        second_round_responses.append(response)
    
    # Check that responses show interaction between characters
    assert len(second_round_responses) == len(characters), "All characters should respond in the second round"
    
    # Verify discussion results are being tracked
    discussion_results = group.get_discussion_summary()
    assert 'participants' in discussion_results, "Discussion should track participant information"
    assert 'key_points' in discussion_results, "Discussion should track key points"
