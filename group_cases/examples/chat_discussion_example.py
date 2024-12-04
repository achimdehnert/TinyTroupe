"""
Example of using chat interface and word processing in discussions.
"""
from group_cases.src.core.base_discussion import BaseDiscussion, DiscussionType
from group_cases.src.tools.chat_interface import ChatInterface
from group_cases.src.tools.word_processor import WordProcessor
import json
import os
from datetime import datetime

class ChatBasedDiscussion(BaseDiscussion):
    """Discussion implementation using chat interface."""
    
    def __init__(self, name: str, discussion_type: DiscussionType):
        super().__init__(name, discussion_type)
        self.chat = ChatInterface(self, self._handle_message)
        self.processor = WordProcessor()
        self.analysis_results = []
        
    def _handle_message(self, message):
        """Handle incoming chat messages."""
        # Analyze message content
        analysis = self.processor.analyze_text(message.content)
        
        # Store analysis results
        self.analysis_results.append({
            "timestamp": message.timestamp.isoformat(),
            "sender": message.sender,
            "analysis": analysis
        })
        
        # Generate and send summary if needed
        if len(self.chat.messages) % 5 == 0:  # Every 5 messages
            recent_messages = self.chat.get_chat_history(limit=5)
            combined_text = "\n".join(
                msg["content"] for msg in recent_messages
            )
            summary = self.processor.generate_summary(combined_text)
            
            self.chat.send_message(
                f"Summary of recent discussion:\n{summary}",
                "system",
                "summary"
            )

def main():
    # Create discussion
    discussion = ChatBasedDiscussion(
        "Product Feature Planning",
        DiscussionType.BRAINSTORMING
    )
    
    # Add participants
    participants = [
        ("moderator", "Moderator"),
        ("dev1", "Developer"),
        ("designer1", "Designer"),
        ("pm1", "Product Manager")
    ]
    
    for user_id, role in participants:
        discussion.chat.add_user(user_id, role)
    
    # Simulate discussion
    messages = [
        ("moderator", "Welcome everyone! Today we'll discuss new features for Q3."),
        ("pm1", "I think we should focus on user engagement features."),
        ("designer1", "We could add interactive tutorials for new users."),
        ("dev1", "That's feasible. We can use our existing onboarding framework."),
        ("pm1", "Great idea! Could we also add progress tracking?"),
        ("designer1", "Yes, and gamification elements would make it more engaging."),
        ("dev1", "We'd need to design a flexible achievement system."),
        ("moderator", "Let's break this down into concrete tasks.")
    ]
    
    # Send messages
    for sender, content in messages:
        discussion.chat.send_message(content, sender)
    
    # Export chat history
    output_dir = "data/chat_logs"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chat_file = os.path.join(output_dir, f"discussion_{timestamp}.json")
    discussion.chat.export_chat(chat_file)
    
    # Generate formatted transcript
    processor = WordProcessor()
    chat_history = discussion.chat.get_chat_history()
    
    # Save in different formats
    for format_type in ["markdown", "html", "plain"]:
        formatted = processor.format_discussion(
            chat_history,
            format_type
        )
        
        output_file = os.path.join(
            output_dir,
            f"transcript_{timestamp}.{format_type}"
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted)
    
    # Print analysis
    print("\nDiscussion Analysis:")
    print("-" * 50)
    
    all_text = "\n".join(msg["content"] for msg in chat_history)
    analysis = processor.analyze_text(all_text)
    
    print(f"Total Words: {analysis['word_count']}")
    print(f"Unique Words: {analysis['unique_words']}")
    print(f"Readability Score: {analysis['readability_score']:.2f}")
    print("\nKey Points:")
    for point in processor.extract_key_points(all_text):
        print(f"- {point}")
    
    print("\nKeyword Frequency:")
    for word, freq in analysis['keyword_frequency'].items():
        print(f"- {word}: {freq}")

if __name__ == "__main__":
    main()
