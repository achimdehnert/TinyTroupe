"""
Module for managing character interactions in the enhanced group memory app.
This integrates the TinyTroupe character system with our group discussion functionality.
"""

import os
import sys
from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import random

# Add TinyTroupe to Python path
tinytroupe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, tinytroupe_path)

from group_cases.src.core.characters import TinyPerson, EpisodicMemory, RecallFaculty, FilesAndWebGroundingFaculty
from tinytroupe.memory import EnhancedSemanticMemory
from group_cases.src.core.environment import TinyWorld
from .discussion import GroupDiscussion, MessageType, DiscussionType

__all__ = [
    'Character',
    'CharacterGroup',
    'create_lisa_the_data_scientist',
    'create_oscar_the_architect',
    'create_maya_the_psychologist',
    'create_alex_the_entrepreneur',
    'create_sophia_the_biotech_researcher',
    'create_marcus_the_game_designer',
    'create_amira_the_environmental_scientist',
    'create_raj_the_ai_ethicist',
    'create_elena_the_urban_planner'
]

@dataclass
class Character:
    """Represents a character in the discussion."""
    name: str
    age: int
    occupation: str
    nationality: str
    interests: List[str]
    personality: List[str]
    tiny_person: TinyPerson = None
    _unique_id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S_%f"))

    def __post_init__(self):
        """Initialize the TinyPerson instance with character traits."""
        if not self.tiny_person:
            # Create TinyPerson instance with mental faculties
            unique_name = f"{self.name.replace(' ', '_')}_{self._unique_id}"
            self.tiny_person = TinyPerson(
                name=unique_name,
                mental_faculties=[
                    RecallFaculty(),
                    FilesAndWebGroundingFaculty()
                ],
                episodic_memory=EpisodicMemory(),
                semantic_memory=EnhancedSemanticMemory()
            )

            # Configure character traits and background
            self._configure_character_traits()
            
            # Initialize the prompt
            self.tiny_person.reset_prompt()

    def _configure_character_traits(self):
        """Configure the character's traits and background in TinyPerson."""
        # Create a rich background description
        background = self._generate_background_description()
        
        # Update TinyPerson configuration
        self.tiny_person._configuration.update({
            "name": self.name.replace(" ", "_"),
            "age": self.age,
            "nationality": self.nationality,
            "occupation": self.occupation,
            "occupation_description": self._generate_occupation_description(),
            "personality_traits": self.personality,
            "professional_interests": [int for int in self.interests if not int.lower() in ['music', 'sports', 'arts', 'photography', 'rock climbing', 'martial arts']],
            "personal_interests": [int for int in self.interests if int.lower() in ['music', 'sports', 'arts', 'photography', 'rock climbing', 'martial arts']],
            "background": background,
            "communication_style": self._derive_communication_style(),
            "current_context": "Ready to engage in meaningful discussion"
        })

        # Store character information in semantic memory
        self.tiny_person.semantic_memory.store({
            'character_profile': {
                'name': self.name,
                'background': background,
                'traits': self.personality,
                'expertise': self.occupation,
                'interests': self.interests
            }
        })

    def _generate_background_description(self) -> str:
        """Generate a detailed background description for the character."""
        return f"{self.name} is a {self.age}-year-old {self.nationality} {self.occupation}. " \
               f"They are known for being {', '.join(self.personality[:-1])} and {self.personality[-1]}. " \
               f"Their expertise spans across {', '.join(self.interests[:-1])} and {self.interests[-1]}."

    def _generate_occupation_description(self) -> str:
        """Generate a detailed description of the character's occupation."""
        occupation_descriptions = {
            "Senior Data Scientist": "specializes in advanced machine learning and data analytics, focusing on ethical AI development and practical applications of statistical analysis",
            "Sustainable Architecture Specialist": "focuses on designing environmentally conscious buildings and urban spaces, integrating renewable materials and sustainable practices",
            "Clinical Psychologist": "helps individuals and groups navigate complex emotional and behavioral challenges using evidence-based therapeutic approaches",
            "Tech Startup Founder": "leads innovative technology initiatives, combining entrepreneurial vision with practical business strategy and technical expertise"
        }
        return occupation_descriptions.get(self.occupation, f"works as a {self.occupation}, bringing expertise and innovation to their field")

    def _derive_communication_style(self) -> dict:
        """Derive the character's communication style based on their personality traits."""
        style = {
            "formality_level": "formal" if "professional" in self.personality else "casual",
            "detail_orientation": "high" if "detail-oriented" in self.personality else "moderate",
            "emotional_expression": "high" if any(trait in self.personality for trait in ["empathetic", "energetic"]) else "moderate",
            "technical_language": "high" if self.occupation in ["Senior Data Scientist", "Sustainable Architecture Specialist"] else "moderate"
        }
        return style

class CharacterGroup:
    """Manages a group of characters participating in a discussion."""
    
    def __init__(self, characters: List[Character]):
        """Initialize the character group."""
        self.characters = characters
        self.discussion_results = {
            'insights': [],
            'key_points': [],
            'sentiment_analysis': []
        }
        
        # Clear all existing environments
        TinyWorld.clear_environments()
        
        # Create a unique environment name
        env_name = f"Discussion_Room_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Create the world with the unique name
        self.world = TinyWorld(env_name)
        
        # Add all characters to the environment
        for char in self.characters:
            try:
                self.world.add_agent(char.tiny_person)
            except ValueError as e:
                # If agent already exists, recreate it with a new unique name
                char.tiny_person = None
                char.__post_init__()
                self.world.add_agent(char.tiny_person)
                
        self.world.make_everyone_accessible()
    
    def start_discussion(self, topic: str, initial_prompt: str) -> GroupDiscussion:
        """Start a new group discussion with the characters."""
        discussion = GroupDiscussion(
            discussion_name=topic,
            discussion_type=DiscussionType.CUSTOM,
            context=f"Character interaction discussion about: {topic}"
        )
        
        # Add the initial prompt as a system message
        discussion.chat_interface.add_message(
            sender="System",
            content=initial_prompt,
            msg_type=MessageType.SYSTEM
        )
        
        # Initialize the discussion context for all characters
        context = f"""Topic of discussion: {topic}
Initial prompt: {initial_prompt}

You are participating in a discussion about {topic}. 
As an expert in your field, provide thoughtful insights and engage with others' perspectives.
Focus on how your unique background and expertise can contribute to the discussion."""

        # Have each character process the initial prompt
        for char in self.characters:
            # Set character context and goals
            char.tiny_person.change_context([context])
            char.tiny_person.internalize_goal([
                f"Engage in a meaningful discussion about {topic}",
                f"Share expertise as a {char.occupation}",
                "Respond thoughtfully to others' perspectives"
            ])
            
            # Generate character's initial response
            response = self._generate_character_response(char, initial_prompt, discussion)
            
            if response:
                discussion.chat_interface.add_message(
                    sender=char.name,
                    content=response,
                    msg_type=MessageType.TEXT
                )
                self._update_discussion_results(char, response)

        return discussion

    def _generate_character_response(self, character: Character, prompt: str, discussion: GroupDiscussion) -> str:
        """Generate a response from a character based on their expertise and personality."""
        # Create a detailed context for the character
        context = self._create_response_context(character, prompt, discussion)
        
        # Have the character process the context
        character.tiny_person.change_context([context])
        
        # Create a specific goal for the character to respond
        goal_str = (
            f"Respond thoughtfully to the discussion about {discussion.discussion_name} "
            f"by sharing insights based on my expertise as a {character.occupation} "
            "and engaging meaningfully with the conversation."
        )
        character.tiny_person.internalize_goal(goal_str)

        # Add a thought to help guide the response
        thought = (
            f"As a {character.occupation}, I should provide a thoughtful response about {discussion.discussion_name} "
            f"based on my expertise in {', '.join(character.interests)}."
        )
        character.tiny_person.think(thought)
        
        # Generate the response action
        actions = character.tiny_person.listen_and_act(prompt, return_actions=True)
        
        # Extract response from actions, prioritizing TALK actions
        response = None
        if actions:
            # First try to find direct TALK actions
            for action in actions:
                if isinstance(action, dict) and 'action' in action:
                    action_data = action['action']
                    if action_data.get('type') == 'TALK' and action_data.get('content'):
                        response = action_data['content']
                        break
            
            # If no TALK action found, try other action types
            if not response:
                response = self._extract_response_from_actions(actions)
            
            # If still no response, use fallback
            if not response:
                response = self._generate_fallback_response(character, prompt)
            
            # Store the response in character's memory
            if response:
                character.tiny_person.episodic_memory.store({
                    'role': 'assistant',
                    'name': character.name,
                    'content': response,
                    'timestamp': datetime.now().isoformat(),
                    'context': context,
                    'discussion_topic': discussion.discussion_name
                })
        
        return response

    def _create_response_context(self, character: Character, prompt: str, discussion: GroupDiscussion) -> str:
        """Create a detailed context for character response generation."""
        recent_messages = discussion.chat_interface.messages[-5:] if discussion.chat_interface.messages else []
        
        context = f"""As {character.name}, a {character.occupation} with expertise in {', '.join(character.interests)}, 
you are participating in a discussion about {discussion.discussion_name}.

Your personality traits are: {', '.join(character.personality)}
Your background: {character._generate_background_description()}

Current discussion context:
{prompt}

Recent messages:
"""
        for msg in recent_messages:
            context += f"{msg.sender}: {msg.content}\n"
            
        return context

    def _extract_response_from_actions(self, actions: list) -> str:
        """Extract response from character actions."""
        if not actions:
            return None

        # First try to find direct speech actions    
        for action in actions:
            if isinstance(action, str):
                # Handle string actions (TinyTroupe format)
                if '[TALK]' in action:
                    parts = action.split('[TALK]')
                    if len(parts) > 1:
                        response = parts[1].strip().lstrip('> ')
                        if response:
                            return response
                elif '[SAY]' in action:
                    parts = action.split('[SAY]')
                    if len(parts) > 1:
                        response = parts[1].strip().lstrip('> ')
                        if response:
                            return response
            elif isinstance(action, dict):
                # Handle dictionary actions
                if action.get('type') in ['SPEAK', 'TALK', 'SAY']:
                    if 'content' in action and action['content']:
                        return action['content']
                    elif 'text' in action and action['text']:
                        return action['text']
                    elif 'lines' in action and action['lines']:
                        return '\n'.join(action['lines'])

        # If no direct speech found, try thought actions
        for action in actions:
            if isinstance(action, str):
                if '[THINK]' in action:
                    parts = action.split('[THINK]')
                    if len(parts) > 1:
                        response = parts[1].strip().lstrip('> ')
                        if response:
                            return response
            elif isinstance(action, dict):
                if action.get('type') == 'THINK':
                    if 'content' in action and action['content']:
                        return action['content']
                    elif 'text' in action and action['text']:
                        return action['text']
                    elif 'lines' in action and action['lines']:
                        return '\n'.join(action['lines'])

        # If no speech or thought actions found, try to extract any meaningful text
        for action in actions:
            if isinstance(action, str):
                # Remove any action markers and check if there's content
                cleaned = action.split(']')[-1].strip().lstrip('> ')
                if cleaned:
                    return cleaned
            elif isinstance(action, dict):
                # Try to find any content in the dictionary
                for key in ['response', 'message', 'output', 'result']:
                    if key in action and action[key]:
                        return str(action[key])

        return None

    def _generate_fallback_response(self, character: Character, prompt: str) -> str:
        """Generate a fallback response based on character traits when normal response generation fails."""
        # Create response templates based on occupation
        occupation_templates = {
            "Senior Data Scientist": [
                "From a data-driven perspective, {prompt}",
                "Looking at this analytically, {prompt}",
                "The data suggests that {prompt}"
            ],
            "Sustainable Architecture Specialist": [
                "From a sustainable design standpoint, {prompt}",
                "Considering environmental impact, {prompt}",
                "In architectural terms, {prompt}"
            ]
        }
        
        # Select template based on character's occupation
        templates = occupation_templates.get(character.occupation, [
            "Based on my experience as a {occupation}, {prompt}",
            "From my perspective in {occupation}, {prompt}",
            "As someone working in {occupation}, {prompt}"
        ])
        
        # Generate response using template
        template = random.choice(templates)
        response = template.format(
            occupation=character.occupation,
            prompt=prompt
        )
        
        return response

    def get_character_response(self, character: Character, discussion: GroupDiscussion) -> str:
        """Get a response from a character based on the discussion context."""
        # Get the recent discussion history
        recent_messages = discussion.chat_interface.messages[-5:] if len(discussion.chat_interface.messages) > 0 else []
        
        # Format the discussion context
        discussion_context = f"""
Topic: {discussion.discussion_name}
Current Discussion:
"""
        for msg in recent_messages:
            discussion_context += f"{msg.sender}: {msg.content}\n"
        
        # Create detailed context for response generation
        context = self._create_response_context(character, discussion_context, discussion)
        
        # Have the character process the context
        character.tiny_person.change_context([context])
        actions = character.tiny_person.listen_and_act(discussion_context, return_actions=True)
        
        # Extract response from actions
        response = self._extract_response_from_actions(actions)
        
        if not response:
            # Fallback response generation
            response = self._generate_fallback_response(character, discussion_context)
        
        if response:
            # Store the response in character's memory
            character.tiny_person.episodic_memory.store({
                'role': 'assistant',
                'name': character.name,
                'content': response,
                'timestamp': datetime.now().isoformat(),
                'context': context,
                'discussion_topic': discussion.discussion_name
            })
            
            # Update discussion results
            self._update_discussion_results(character, response)
        
        return response
    
    def _update_discussion_results(self, character: Character, response: str):
        """Update discussion results with new insights and analysis."""
        # Store the response in character's memory with additional metadata
        character.tiny_person.episodic_memory.store({
            'role': 'assistant',
            'name': character.name,
            'content': response,
            'timestamp': datetime.now().isoformat(),
            'type': 'discussion_contribution',
            'metadata': {
                'occupation': character.occupation,
                'interests': character.interests,
                'personality': character.personality
            }
        })

        # Extract insights and key points
        if len(response) > 0:
            # Add the insight with metadata
            insight = {
                'character': character.name,
                'content': response,
                'timestamp': datetime.now().isoformat(),
                'expertise': character.occupation,
                'traits': character.personality
            }
            self.discussion_results['insights'].append(insight)
            
            # Perform basic sentiment analysis
            sentiment = self._analyze_sentiment(response)
            self.discussion_results['sentiment_analysis'].append({
                'character': character.name,
                'sentiment': sentiment,
                'timestamp': datetime.now().isoformat()
            })
            
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis based on keyword presence."""
        positive_words = {'great', 'good', 'excellent', 'agree', 'positive', 'interesting', 'helpful', 'valuable', 'excited'}
        negative_words = {'bad', 'disagree', 'negative', 'wrong', 'difficult', 'concerned', 'worried', 'problematic'}
        
        words = set(text.lower().split())
        positive_count = len(words.intersection(positive_words))
        negative_count = len(words.intersection(negative_words))
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        return 'neutral'
    
    def get_discussion_summary(self) -> dict:
        """Get a summary of the discussion results with enhanced analytics."""
        summary = {
            'insights': self.discussion_results['insights'],
            'sentiment_analysis': self.discussion_results['sentiment_analysis'],
            'participation': self._analyze_participation(),
            'interaction_patterns': self._analyze_interaction_patterns(),
            'timestamp': datetime.now().isoformat()
        }
        return summary

    def _analyze_participation(self) -> dict:
        """Analyze participation patterns in the discussion."""
        participation = {}
        for char in self.characters:
            char_messages = [msg for msg in self.discussion_results['insights'] 
                           if msg['character'] == char.name]
            participation[char.name] = {
                'message_count': len(char_messages),
                'expertise_utilized': char.occupation,
                'last_contribution': char_messages[-1]['timestamp'] if char_messages else None
            }
        return participation

    def _analyze_interaction_patterns(self) -> dict:
        """Analyze interaction patterns between characters."""
        patterns = {
            'sentiment_trends': self._get_sentiment_trends(),
            'discussion_flow': self._get_discussion_flow()
        }
        return patterns

    def _get_sentiment_trends(self) -> dict:
        """Analyze sentiment trends over time."""
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        for analysis in self.discussion_results['sentiment_analysis']:
            sentiment_counts[analysis['sentiment']] += 1
        
        return {
            'overall_sentiment': max(sentiment_counts.items(), key=lambda x: x[1])[0],
            'sentiment_distribution': sentiment_counts
        }

    def _get_discussion_flow(self) -> list:
        """Analyze the flow of discussion between characters."""
        flow = []
        insights = sorted(self.discussion_results['insights'], 
                        key=lambda x: x['timestamp'])
        
        for i in range(len(insights) - 1):
            current = insights[i]
            next_insight = insights[i + 1]
            flow.append({
                'from': current['character'],
                'to': next_insight['character'],
                'timestamp': next_insight['timestamp']
            })
        
        return flow

# Example character definitions
def create_lisa_the_data_scientist() -> Character:
    """Create Lisa, an experienced data scientist character."""
    return Character(
        name="Lisa Chen",
        age=32,
        occupation="Senior Data Scientist",
        nationality="Canadian-Chinese",
        interests=[
            "machine learning",
            "data visualization",
            "statistical analysis",
            "ethical AI",
            "tech education",
            "rock climbing"
        ],
        personality=[
            "analytical",
            "detail-oriented",
            "collaborative",
            "innovative",
            "patient teacher"
        ]
    )

def create_oscar_the_architect() -> Character:
    """Create Oscar, a creative architect character."""
    return Character(
        name="Oscar Rodriguez",
        age=45,
        occupation="Sustainable Architecture Specialist",
        nationality="Spanish",
        interests=[
            "sustainable design",
            "urban planning",
            "environmental psychology",
            "traditional craftsmanship",
            "renewable materials",
            "photography"
        ],
        personality=[
            "creative",
            "environmentally conscious",
            "pragmatic",
            "visionary",
            "articulate"
        ]
    )

def create_maya_the_psychologist() -> Character:
    """Create Maya, an insightful psychologist character."""
    return Character(
        name="Maya Patel",
        age=38,
        occupation="Clinical Psychologist",
        nationality="British-Indian",
        interests=[
            "cognitive behavioral therapy",
            "group dynamics",
            "mindfulness",
            "cultural psychology",
            "art therapy",
            "classical music"
        ],
        personality=[
            "empathetic",
            "observant",
            "thoughtful",
            "culturally aware",
            "good listener"
        ]
    )

def create_alex_the_entrepreneur() -> Character:
    """Create Alex, a dynamic tech entrepreneur character."""
    return Character(
        name="Alex Kim",
        age=29,
        occupation="Tech Startup Founder",
        nationality="Korean-American",
        interests=[
            "startup ecosystems",
            "blockchain technology",
            "product design",
            "venture capital",
            "social impact",
            "martial arts"
        ],
        personality=[
            "ambitious",
            "adaptable",
            "risk-taker",
            "strategic thinker",
            "energetic"
        ]
    )

def create_sophia_the_biotech_researcher() -> Character:
    """Create Sophia, a pioneering biotech researcher."""
    return Character(
        name="Sophia Weber",
        age=41,
        occupation="Biotechnology Researcher",
        nationality="German",
        interests=[
            "genetic engineering",
            "synthetic biology",
            "bioethics",
            "medical innovation",
            "science communication",
            "hiking"
        ],
        personality=[
            "meticulous",
            "forward-thinking",
            "ethical",
            "curious",
            "collaborative"
        ]
    )

def create_marcus_the_game_designer() -> Character:
    """Create Marcus, an innovative game designer."""
    return Character(
        name="Marcus Thompson",
        age=34,
        occupation="Game Design Director",
        nationality="Australian",
        interests=[
            "game mechanics",
            "player psychology",
            "virtual reality",
            "storytelling",
            "indie games",
            "surfing"
        ],
        personality=[
            "creative",
            "playful",
            "user-focused",
            "team leader",
            "problem-solver"
        ]
    )

def create_amira_the_environmental_scientist() -> Character:
    """Create Amira, a passionate environmental scientist."""
    return Character(
        name="Amira Hassan",
        age=36,
        occupation="Environmental Scientist",
        nationality="Egyptian",
        interests=[
            "climate change",
            "sustainable development",
            "water conservation",
            "renewable energy",
            "environmental policy",
            "desert ecology"
        ],
        personality=[
            "passionate",
            "data-driven",
            "advocacy-oriented",
            "diplomatic",
            "determined"
        ]
    )

def create_raj_the_ai_ethicist() -> Character:
    """Create Raj, an AI ethics specialist."""
    return Character(
        name="Raj Malhotra",
        age=43,
        occupation="AI Ethics Consultant",
        nationality="Indian",
        interests=[
            "AI governance",
            "digital rights",
            "philosophy of mind",
            "cross-cultural ethics",
            "responsible innovation",
            "classical indian music"
        ],
        personality=[
            "philosophical",
            "balanced",
            "analytical",
            "inclusive",
            "thought leader"
        ]
    )

def create_elena_the_urban_planner() -> Character:
    """Create Elena, a visionary urban planner."""
    return Character(
        name="Elena Popov",
        age=39,
        occupation="Smart City Planner",
        nationality="Russian",
        interests=[
            "smart cities",
            "public transportation",
            "social architecture",
            "community engagement",
            "urban agriculture",
            "ballet"
        ],
        personality=[
            "visionary",
            "community-oriented",
            "practical",
            "innovative",
            "collaborative"
        ]
    )
