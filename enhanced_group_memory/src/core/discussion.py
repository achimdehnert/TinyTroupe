"""
Core discussion system that manages different types of group discussions.
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
from .memory import EnhancedMemorySystem, Memory

class MessageType(Enum):
    TEXT = "text"
    SYSTEM = "system"
    REACTION = "reaction"

class Message:
    def __init__(self, sender: str, content: str, msg_type: MessageType = MessageType.TEXT):
        self.sender = sender
        self.content = content
        self.msg_type = msg_type
        self.timestamp = datetime.now()
        self.reactions: Dict[str, List[str]] = {}  # reaction -> list of users

class DiscussionType(Enum):
    FOCUS_GROUP = "focus_group"
    INTERVIEW = "interview"
    BRAINSTORMING = "brainstorming"
    EVALUATION = "evaluation"
    CUSTOM = "custom"

class ChatInterface:
    def __init__(self):
        self.messages: List[Message] = []
        self.memory_system = EnhancedMemorySystem()
        
    def add_message(self, sender: str, content: str, msg_type: MessageType = MessageType.TEXT):
        """Add a new message to the chat."""
        message = Message(sender, content, msg_type)
        self.messages.append(message)
        
        # Store message in memory system
        context = {
            "sender": sender,
            "type": msg_type.value,
            "discussion_time": len(self.messages)
        }
        self.memory_system.store_episodic_memory(content, context)
        
    def add_reaction(self, message_index: int, reaction: str, user: str):
        """Add a reaction to a message."""
        if 0 <= message_index < len(self.messages):
            message = self.messages[message_index]
            if reaction not in message.reactions:
                message.reactions[reaction] = []
            if user not in message.reactions[reaction]:
                message.reactions[reaction].append(user)
                
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics data about the discussion."""
        analytics = {
            "total_messages": len(self.messages),
            "active_users": len({msg.sender for msg in self.messages}),
            "messages_per_user": {},
            "reactions_per_message": [],
            "topic_evolution": self._analyze_topics(),
            "interaction_patterns": self._analyze_interactions()
        }
        
        # Count messages per user
        for msg in self.messages:
            if msg.sender not in analytics["messages_per_user"]:
                analytics["messages_per_user"][msg.sender] = 0
            analytics["messages_per_user"][msg.sender] += 1
            
        # Count reactions per message
        for msg in self.messages:
            total_reactions = sum(len(users) for users in msg.reactions.values())
            analytics["reactions_per_message"].append(total_reactions)
            
        return analytics
    
    def _analyze_topics(self) -> Dict[str, Any]:
        """Analyze topic evolution over time."""
        # Use memory system to find related messages and extract topics
        windows = []
        window_size = max(5, len(self.messages) // 4)
        
        for i in range(0, len(self.messages), window_size):
            window_messages = self.messages[i:i + window_size]
            if not window_messages:
                continue
                
            # Combine messages and find related memories
            combined_text = " ".join(msg.content for msg in window_messages)
            related_memories = self.memory_system.search_memories(combined_text, k=3)
            
            window_data = {
                "timestamp_start": window_messages[0].timestamp,
                "timestamp_end": window_messages[-1].timestamp,
                "key_terms": self._extract_key_terms(combined_text),
                "sentiment": 0.0  # Placeholder for sentiment analysis
            }
            windows.append(window_data)
            
        return {"windows": windows}
    
    def _analyze_interactions(self) -> Dict[str, Any]:
        """Analyze interaction patterns between users."""
        interaction_matrix = {}
        
        for i, msg in enumerate(self.messages):
            if msg.sender not in interaction_matrix:
                interaction_matrix[msg.sender] = {}
                
            # Look for replies (messages that follow within 2 messages)
            for j in range(i + 1, min(i + 3, len(self.messages))):
                reply = self.messages[j]
                if reply.sender != msg.sender:
                    if reply.sender not in interaction_matrix[msg.sender]:
                        interaction_matrix[msg.sender][reply.sender] = 0
                    interaction_matrix[msg.sender][reply.sender] += 1
                    
        return {"interaction_matrix": interaction_matrix}
    
    def _extract_key_terms(self, text: str) -> Dict[str, float]:
        """Extract key terms and their importance from text."""
        # Placeholder for key term extraction
        # In a real implementation, you might use techniques like TF-IDF or KeyBERT
        return {"term1": 1.0, "term2": 0.8}  # Placeholder

class GroupDiscussion:
    """Base class for all discussion types."""
    def __init__(self, 
                 discussion_name: str,
                 discussion_type: DiscussionType,
                 context: str = ""):
        self.discussion_name = discussion_name
        self.discussion_type = discussion_type
        self.context = context
        self.chat_interface = ChatInterface()
        self.results: Dict[str, Any] = {}
        
    def add_message(self, sender: str, content: str):
        """Add a message to the discussion."""
        self.chat_interface.add_message(sender, content)
        
    def get_results(self) -> Dict[str, Any]:
        """Get discussion results."""
        return self.results
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get discussion analytics."""
        return self.chat_interface.get_analytics()
    
    def search_discussion(self, query: str) -> List[Memory]:
        """Search through discussion history."""
        return self.chat_interface.memory_system.search_memories(query)
    
    def consolidate_memories(self) -> List[Memory]:
        """Consolidate discussion memories."""
        return self.chat_interface.memory_system.consolidate_memories()

class ApartmentAdDiscussion(GroupDiscussion):
    def __init__(self, apartment_description: str):
        super().__init__(
            "Apartment Ad Discussion",
            DiscussionType.FOCUS_GROUP,
            "Creating an effective apartment rental advertisement"
        )
        self.chat_interface.add_message(
            "System",
            f"Discussion started for apartment:\n{apartment_description}",
            MessageType.SYSTEM
        )

class ProductBrainstormingDiscussion(GroupDiscussion):
    def __init__(self, product_name: str, industry: str):
        super().__init__(
            f"{product_name} Feature Brainstorming",
            DiscussionType.BRAINSTORMING,
            f"Brainstorming innovative AI features for {product_name}"
        )
        self.chat_interface.add_message(
            "System",
            f"Brainstorming session started for {product_name} in {industry}",
            MessageType.SYSTEM
        )

class CustomerInterviewDiscussion(GroupDiscussion):
    def __init__(self, company_context: str, customer_profile: str):
        super().__init__(
            "Customer Interview",
            DiscussionType.INTERVIEW,
            company_context
        )
        self.chat_interface.add_message(
            "System",
            f"Interview started with customer profile:\n{customer_profile}",
            MessageType.SYSTEM
        )

class AdEvaluationDiscussion(GroupDiscussion):
    def __init__(self, product_type: str, ads: List[str]):
        super().__init__(
            f"{product_type} Ad Evaluation",
            DiscussionType.EVALUATION,
            f"Evaluating advertisements for {product_type}"
        )
        for i, ad in enumerate(ads, 1):
            self.chat_interface.add_message(
                "System",
                f"Ad {i}:\n{ad}",
                MessageType.SYSTEM
            )
