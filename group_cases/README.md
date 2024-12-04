# Group Cases Framework

## Overview

Group Cases is an advanced collaborative discussion and analysis framework designed to facilitate complex group interactions, knowledge management, and insights generation.

## Key Components

### 1. Chat Interface (`tools/chat_interface.py`)
- Advanced messaging system
- Support for multiple message types
- Threading capabilities
- Reaction mechanisms
- User activity tracking

### 2. Discussion Analytics (`tools/advanced_analytics.py`)
- Comprehensive discussion dynamics analysis
- Participation metrics
- Topic evolution tracking
- Sentiment analysis
- Interaction pattern recognition

### 3. Streamlit Frontend (`src/streamlit_app.py`)
- Interactive chat interface
- Real-time message display
- User customization
- Potential for analytics visualization

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/TinyTroupe.git

# Navigate to the project directory
cd TinyTroupe

# Install in editable mode
pip install -e .
```

## Usage Examples

### Basic Chat Interface

```python
from group_cases.src.tools.chat_interface import ChatInterface, MessageType

# Initialize chat interface
chat = ChatInterface()

# Add messages
chat.add_message(
    sender="Alice", 
    content="Hello, everyone!", 
    msg_type=MessageType.TEXT
)

# Create a thread
thread_id = chat.create_thread(0)  # Create thread from first message

# Add reactions
chat.add_reaction(
    message_index=0, 
    user="Bob", 
    reaction="👍"
)
```

### Advanced Analytics

```python
# Get discussion analytics
analytics = chat.get_analytics()
print(analytics['total_messages'])
print(analytics['messages_per_user'])
```

## Features

- 🌐 Flexible Messaging
- 📊 Advanced Analytics
- 🧵 Threading Support
- 😀 Reaction System
- 🔍 Detailed User Tracking

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/TinyTroupe](https://github.com/yourusername/TinyTroupe)
