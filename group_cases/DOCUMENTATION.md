# Group Cases Framework: User Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
3. [Chat Interface](#chat-interface)
4. [Discussion Analytics](#discussion-analytics)
5. [Streamlit Frontend](#streamlit-frontend)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)

## Introduction

The Group Cases Framework is a sophisticated platform designed to enhance group discussions, knowledge management, and collaborative analysis. It provides powerful tools for tracking, analyzing, and understanding group interactions.

## Core Concepts

### Message Types
- `TEXT`: Standard text messages
- `SYSTEM`: System-generated messages
- `ACTION`: Action-based messages
- `REACTION`: Reaction to existing messages
- `THREAD`: Threaded discussions
- `MEDIA`: Media-rich messages

### Key Features
- Dynamic message threading
- User activity tracking
- Advanced analytics
- Flexible message interactions

## Chat Interface

### Basic Usage

```python
from group_cases.src.tools.chat_interface import ChatInterface, MessageType

# Initialize chat
chat = ChatInterface()

# Add a message
chat.add_message(
    sender="User1", 
    content="Hello, team!", 
    msg_type=MessageType.TEXT
)

# Create a thread
thread_id = chat.create_thread(0)

# Add a reaction
chat.add_reaction(
    message_index=0, 
    user="User2", 
    reaction="👍"
)
```

### Advanced Methods
- `get_message_history()`: Filter messages
- `get_active_users()`: Track user activity
- `export_chat_history()`: Export discussions

## Discussion Analytics

### Metrics Tracked
- Total message count
- Messages per user
- User participation
- Discussion sentiment
- Topic evolution
- Interaction patterns

### Example

```python
# Get comprehensive analytics
analytics = chat.get_analytics()

# Explore metrics
print(f"Total Messages: {analytics['total_messages']}")
print(f"Active Users: {analytics['active_users']}")
print(f"User Participation: {analytics['messages_per_user']}")
```

## Streamlit Frontend

### Features
- Interactive chat interface
- Real-time message display
- User customization
- Potential analytics visualization

### Running the Frontend
```bash
streamlit run group_cases/src/streamlit_app.py
```

## Advanced Usage

### Custom Message Processing
```python
# Create custom message handlers
def process_message(message):
    # Implement custom logic
    pass

chat.add_message_processor(process_message)
```

### Extending Analytics
```python
# Create custom analytics modules
class CustomAnalytics:
    def analyze(self, messages):
        # Implement custom analysis
        pass
```

## Troubleshooting

### Common Issues
- Import errors: Ensure package is installed in editable mode
- Streamlit not running: Check Python and package versions
- Analytics not working: Verify message data integrity

### Debugging
- Use `print()` statements
- Check `chat.get_analytics()` output
- Validate message types and content

## Best Practices
- Use consistent message types
- Leverage threading for complex discussions
- Regularly export and analyze chat history
- Customize analytics to your specific needs

## Performance Considerations
- Large message volumes may impact performance
- Use filtering and pagination for extensive histories
- Consider database integration for scalability

## Future Roadmap
- Machine learning-powered insights
- Enhanced NLP integration
- More advanced visualization tools
- Real-time collaboration features

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Distributed under the MIT License. See `LICENSE` for details.
