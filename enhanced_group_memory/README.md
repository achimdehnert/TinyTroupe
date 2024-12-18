# Enhanced Group Memory System

A powerful system that combines group discussions with enhanced memory capabilities, built with Streamlit.

## Features

- **Group Discussions**
  - Multiple discussion types (Focus Groups, Interviews, Brainstorming, Evaluations)
  - Real-time sentiment analysis
  - Interactive analytics dashboard
  - Export functionality

- **Memory System**
  - Store and retrieve episodic memories
  - Semantic memory consolidation
  - Memory search and retrieval
  - Memory visualization

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
enhanced_group_memory/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── pages/
│   │   │   ├── __init__.py
│   │   │   ├── discussion.py
│   │   │   └── memory.py
│   │   └── components/
│   │       ├── __init__.py
│   │       ├── analytics.py
│   │       └── chat.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── discussion.py
│   │   ├── memory.py
│   │   └── analytics.py
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── db.py
└── tests/
    └── __init__.py
```

## Usage

Run the application:
```bash
streamlit run src/app/main.py
```

## Features

### Group Discussions
- Create and manage different types of group discussions
- Real-time sentiment analysis of messages
- Interactive analytics dashboard
- Export discussion results

### Memory System
- Store new memories with context
- Search existing memories
- Consolidate episodic memories into semantic memories
- Visualize memory connections

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
