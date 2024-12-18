# Group Cases Framework

## Overview

Group Cases is an advanced collaborative discussion and analysis framework designed to facilitate complex group interactions, knowledge management, and insights generation.

## Project Structure

```
group_cases/
├── docs/               # Documentation files
├── examples/           # Example implementations
│   ├── advertisements/  # Advertisement generation examples
│   ├── discussions/     # Group discussion examples
│   └── utils/           # Utility examples
├── src/                # Source code
│   ├── core/           # Core functionality
│   ├── tools/          # Tools and utilities
│   └── streamlit_app.py # Main Streamlit application
└── tests/              # Test files
```

## Key Components

### 1. Core Components (`src/core/`)
- Character and group management
- Discussion frameworks
- Memory and context handling

### 2. Tools (`src/tools/`)
- Chat Interface (`chat_interface.py`)
  - Advanced messaging system
  - Support for multiple message types
  - Threading capabilities
- Analytics (`advanced_analytics.py`)
  - Discussion dynamics analysis
  - Sentiment analysis
  - Interaction patterns
- Word Processing (`word_processor.py`)
  - Text processing utilities
  - Document generation

### 3. Streamlit Frontend (`src/streamlit_app.py`)
- Interactive chat interface
- Real-time analytics dashboard
- User customization options
- Discussion visualization

## Examples

### Advertisement Generation
- TV advertisement creation
- Real estate listing generation
- Travel advertisement creation

### Group Discussions
- Focus group management
- Product brainstorming
- Customer interviews
- Design reviews

### Utilities
- Chat viewing and analysis
- Database utilities
- Synthetic data generation

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/TinyTroupe.git

# Navigate to the project directory
cd TinyTroupe

# Install in editable mode
pip install -e .
```

## Usage

See the `examples/` directory for detailed usage examples in different scenarios.

For a quick start, run the Streamlit application:

```bash
streamlit run group_cases/src/streamlit_app.py
```

## Documentation

Detailed documentation is available in the `docs/` directory:
- Quick Start Guide
- Analytics Documentation
- API Reference
- Example Use Cases

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
