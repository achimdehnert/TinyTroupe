# TinyTroupe Quick Start Guide

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/achimdehnert/TinyTroupe.git
cd TinyTroupe
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (if needed for your LLM integration)

## Running the Application

### Starting the Streamlit App
1. Navigate to the project directory:
```bash
cd group_cases/src
```

2. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

### Basic Usage
1. **Start a Discussion**
   - Click "Start Discussion" in the sidebar
   - Choose characters to participate
   - Set discussion parameters

2. **Interact with Characters**
   - Type messages in the chat input
   - View character responses
   - Observe character interactions

3. **View Analytics**
   - Enable analytics from the sidebar
   - Navigate through different analytics tabs
   - Monitor discussion dynamics

## Key Features

### Character Interaction
- Dynamic character responses based on personality
- Memory-enhanced conversations
- Natural language processing

### Analytics Dashboard
- Real-time participation metrics
- Sentiment analysis
- Topic evolution tracking
- Interaction network visualization

## Common Issues and Solutions

### Issue: Characters not responding
- Check LLM API connection
- Verify character configurations
- Ensure proper initialization

### Issue: Analytics not showing
- Confirm discussion has started
- Check for sufficient message count
- Verify data collection

## Development Setup

### Running Tests
```bash
python -m pytest tests/
```

### Code Structure
- `group_cases/src/`: Main application code
- `enhanced_group_memory/`: Memory system
- `docs/`: Documentation
- `tests/`: Test suite

## Next Steps
1. Explore example notebooks in `examples/`
2. Review analytics documentation in `docs/analytics.md`
3. Check API reference for advanced usage
4. Join development discussions

## Getting Help
- Check documentation in `docs/`
- Review GitHub issues
- Contact maintainers

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes
4. Submit pull request

Remember to follow the project's coding standards and include tests for new features.
