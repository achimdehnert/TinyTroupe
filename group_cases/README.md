# Group Cases Project

A comprehensive framework for conducting AI-powered group discussions, interviews, brainstorming sessions, and evaluations using TinyTroupe.

## Project Structure

```
group_cases/
├── src/                    # Source code
│   ├── group_discussion.py # Main discussion framework
│   └── db_utils.py        # Database utilities
├── examples/              # Example implementations
│   ├── apartment_ad.py    # Real estate ad creation
│   ├── product_brainstorm.py  # Feature brainstorming
│   ├── customer_interview.py  # Customer research
│   └── ad_evaluation.py   # Advertisement analysis
├── data/                  # Data storage
│   └── extractions/       # Extracted results
├── docs/                  # Documentation
├── tests/                 # Test cases
├── .env.example          # Environment variables template
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Quick Start

1. **Setup Environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. **Configure Databases**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
```

3. **Run Examples**
```bash
# Run apartment ad creation
python examples/apartment_ad.py

# Run product brainstorming
python examples/product_brainstorm.py

# Run customer interview
python examples/customer_interview.py

# Run ad evaluation
python examples/ad_evaluation.py
```

## Features

### 1. Discussion Types
- Focus Groups
- One-on-One Interviews
- Product Brainstorming
- Advertisement Evaluation
- Custom Discussions

### 2. Agent Management
- Pre-configured expert agents
- Custom agent generation
- Dynamic agent interactions

### 3. Data Management
- File-based storage (JSON)
- Database integration (MySQL & PostgreSQL)
- Rich metadata support

## Usage Examples

### Create an Apartment Advertisement
```python
from src.group_discussion import ApartmentAdDiscussion

discussion = ApartmentAdDiscussion("""
    Modern 1-bedroom apartment...
    [apartment description]
""")
results = discussion.run_discussion()
discussion.save_results(results, "output.json")
```

### Brainstorm Product Features
```python
from src.group_discussion import ProductBrainstormingDiscussion

discussion = ProductBrainstormingDiscussion(
    "Product Name",
    "industry"
)
results = discussion.run_discussion(num_steps=4)
discussion.save_results(results, "features.json")
```

## Development

### Adding New Discussion Types

1. Create a new class inheriting from `GroupDiscussion`:
```python
class NewDiscussionType(GroupDiscussion):
    def __init__(self, specific_params):
        super().__init__(
            "Discussion Name",
            DiscussionType.CUSTOM
        )
        # Add specific initialization
```

2. Configure extraction and metadata:
```python
self.configure_extraction(
    objective="Your objective",
    fields=["field1", "field2"]
)
```

### Running Tests
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
