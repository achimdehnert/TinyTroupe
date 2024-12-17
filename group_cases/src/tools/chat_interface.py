"""
Enhanced chat interface with advanced features.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from enum import Enum
from dataclasses import dataclass

class MessageType(Enum):
    """Types of messages in the chat."""
    TEXT = "text"
    SYSTEM = "system"
    ACTION = "action"
    REACTION = "reaction"
    THREAD = "thread"
    MEDIA = "media"

@dataclass
class ChatMessage:
    """Represents a chat message."""
    sender: str
    content: str
    timestamp: datetime
    msg_type: MessageType
    thread_id: Optional[str] = None
    parent_id: Optional[str] = None
    reactions: Dict[str, List[str]] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize optional fields."""
        if self.reactions is None:
            self.reactions = {}
        if self.metadata is None:
            self.metadata = {}

class ChatInterface:
    """Enhanced chat interface with advanced features."""
    
    def __init__(self):
        """Initialize chat interface."""
        self.messages: List[ChatMessage] = []
        self.active_users: Dict[str, Dict[str, Any]] = {}
        self.threads: Dict[str, List[ChatMessage]] = {}
        self.reactions_enabled = True
        self.threading_enabled = True
        self.typing_indicators = {}
        
    def add_message(
        self,
        sender: str,
        content: str,
        msg_type: MessageType = MessageType.TEXT,
        thread_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ChatMessage:
        """Add a new message to the chat."""
        message = ChatMessage(
            sender=sender,
            content=content,
            timestamp=datetime.now(),
            msg_type=msg_type,
            thread_id=thread_id,
            parent_id=parent_id,
            reactions={},
            metadata=metadata or {}
        )
        
        self.messages.append(message)
        
        if thread_id:
            if thread_id not in self.threads:
                self.threads[thread_id] = []
            self.threads[thread_id].append(message)
            
        if sender not in self.active_users:
            self.active_users[sender] = {
                "join_time": datetime.now(),
                "message_count": 0,
                "last_active": datetime.now()
            }
        self.active_users[sender]["message_count"] += 1
        self.active_users[sender]["last_active"] = datetime.now()
        
        return message
        
    def add_reaction(
        self,
        message_index: int,
        user: str,
        reaction: str
    ) -> bool:
        """Add a reaction to a message."""
        if not self.reactions_enabled:
            return False
            
        if 0 <= message_index < len(self.messages):
            message = self.messages[message_index]
            if reaction not in message.reactions:
                message.reactions[reaction] = []
            if user not in message.reactions[reaction]:
                message.reactions[reaction].append(user)
            return True
        return False
        
    def create_thread(
        self,
        parent_message_index: int
    ) -> Optional[str]:
        """Create a new thread from a message."""
        if not self.threading_enabled:
            return None
            
        if 0 <= parent_message_index < len(self.messages):
            thread_id = f"thread_{parent_message_index}_{datetime.now().timestamp()}"
            parent_message = self.messages[parent_message_index]
            parent_message.thread_id = thread_id
            self.threads[thread_id] = [parent_message]
            return thread_id
        return None
        
    def set_typing_indicator(self, user: str, is_typing: bool):
        """Set typing indicator for a user."""
        if is_typing:
            self.typing_indicators[user] = datetime.now()
        else:
            self.typing_indicators.pop(user, None)
            
    def get_active_users(self) -> List[Dict[str, Any]]:
        """Get list of active users with their status."""
        current_time = datetime.now()
        active_users = []
        
        for user, data in self.active_users.items():
            time_since_active = (
                current_time - data["last_active"]
            ).total_seconds()
            
            status = {
                "user": user,
                "status": "active" if time_since_active < 300 else "idle",
                "typing": user in self.typing_indicators,
                "message_count": data["message_count"],
                "join_time": data["join_time"].isoformat(),
                "last_active": data["last_active"].isoformat()
            }
            active_users.append(status)
            
        return active_users
        
    def get_thread_messages(
        self,
        thread_id: str
    ) -> List[ChatMessage]:
        """Get messages in a thread."""
        return self.threads.get(thread_id, [])
        
    def get_message_history(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        user: Optional[str] = None,
        msg_type: Optional[MessageType] = None
    ) -> List[ChatMessage]:
        """Get filtered message history."""
        filtered_messages = self.messages
        
        if start_time:
            filtered_messages = [
                msg for msg in filtered_messages
                if msg.timestamp >= start_time
            ]
            
        if end_time:
            filtered_messages = [
                msg for msg in filtered_messages
                if msg.timestamp <= end_time
            ]
            
        if user:
            filtered_messages = [
                msg for msg in filtered_messages
                if msg.sender == user
            ]
            
        if msg_type:
            filtered_messages = [
                msg for msg in filtered_messages
                if msg.msg_type == msg_type
            ]
            
        return filtered_messages
        
    def export_chat_history(
        self,
        format: str = "json",
        include_analytics: bool = False
    ) -> str:
        """Export chat history in specified format."""
        if format == "json":
            history = {
                "messages": [
                    {
                        "sender": msg.sender,
                        "content": msg.content,
                        "timestamp": msg.timestamp.isoformat(),
                        "type": msg.msg_type.value,
                        "thread_id": msg.thread_id,
                        "parent_id": msg.parent_id,
                        "reactions": msg.reactions,
                        "metadata": msg.metadata
                    }
                    for msg in self.messages
                ],
                "threads": {
                    thread_id: [
                        {
                            "sender": msg.sender,
                            "content": msg.content,
                            "timestamp": msg.timestamp.isoformat(),
                            "type": msg.msg_type.value,
                            "reactions": msg.reactions,
                            "metadata": msg.metadata
                        }
                        for msg in thread_messages
                    ]
                    for thread_id, thread_messages in self.threads.items()
                },
                "users": self.get_active_users()
            }
            
            return json.dumps(history, indent=2)
            
        elif format == "markdown":
            lines = []
            for msg in self.messages:
                thread_info = f" (Thread: {msg.thread_id})" if msg.thread_id else ""
                reactions = (
                    f"\nReactions: {', '.join(f'{r}: {len(users)}' for r, users in msg.reactions.items())}"
                    if msg.reactions else ""
                )
                
                lines.append(
                    f"**{msg.sender}** ({msg.timestamp.isoformat()})"
                    f"{thread_info}\n{msg.content}{reactions}\n"
                )
            return "\n".join(lines)
            
        elif format == "html":
            lines = ["<div class='chat-history'>"]
            for msg in self.messages:
                thread_class = f" thread-{msg.thread_id}" if msg.thread_id else ""
                reactions_html = []
                for reaction, users in msg.reactions.items():
                    reactions_html.append(
                        f"<span class='reaction'>{reaction} ({len(users)})</span>"
                    )
                reactions = (
                    f"<div class='reactions'>{''.join(reactions_html)}</div>"
                    if reactions_html else ""
                )
                
                lines.append(
                    f"<div class='message{thread_class}'>"
                    f"<div class='header'>"
                    f"<span class='sender'>{msg.sender}</span>"
                    f"<span class='timestamp'>{msg.timestamp.isoformat()}</span>"
                    f"</div>"
                    f"<div class='content'>{msg.content}</div>"
                    f"{reactions}"
                    f"</div>"
                )
            lines.append("</div>")
            return "\n".join(lines)
            
        raise ValueError(f"Unsupported export format: {format}")
        
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics data for the chat."""
        analytics = {
            "total_messages": len(self.messages),
            "active_users": len(self.active_users),
            "total_threads": 0,  
            "messages_per_user": {},
            "reactions_per_message": [],
            "interaction_patterns": {
                "interaction_matrix": {}
            },
            "topic_evolution": {
                "windows": []
            }
        }
        
        # Calculate messages per user
        for message in self.messages:
            if message.sender not in analytics["messages_per_user"]:
                analytics["messages_per_user"][message.sender] = 0
            analytics["messages_per_user"][message.sender] += 1
            
            # Count reactions
            if message.reactions:
                analytics["reactions_per_message"].append(len(message.reactions))
                
        # Calculate interaction patterns
        for message in self.messages:
            sender = message.sender
            if sender not in analytics["interaction_patterns"]["interaction_matrix"]:
                analytics["interaction_patterns"]["interaction_matrix"][sender] = {}
            
            for other_user in self.active_users:
                if other_user != sender:
                    if other_user not in analytics["interaction_patterns"]["interaction_matrix"][sender]:
                        analytics["interaction_patterns"]["interaction_matrix"][sender][other_user] = 0
                    analytics["interaction_patterns"]["interaction_matrix"][sender][other_user] += 1
        
        # Calculate topic evolution
        window_size = 3  
        for i in range(0, len(self.messages), window_size):
            window_messages = self.messages[i:i+window_size]
            if window_messages:
                window_text = " ".join([msg.content for msg in window_messages])
                sentiment = "positive" if "good" in window_text.lower() else "negative"
                
                words = window_text.lower().split()
                word_freq = {}
                for word in words:
                    if len(word) > 3:  
                        if word not in word_freq:
                            word_freq[word] = 0
                        word_freq[word] += 1
                
                analytics["topic_evolution"]["windows"].append({
                    "timestamp_start": window_messages[0].timestamp.isoformat(),
                    "timestamp_end": window_messages[-1].timestamp.isoformat(),
                    "key_terms": dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]),
                    "sentiment": sentiment
                })
        
        return analytics

def analyze_sentiment(text: str) -> str:
    # This is a placeholder for a sentiment analysis function
    # You can replace this with a real sentiment analysis function
    return "positive" if "good" in text else "negative"
