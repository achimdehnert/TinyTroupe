# TinyTroupe Group Discussion Framework Documentation

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Discussion Types](#discussion-types)
3. [Working with Agents](#working-with-agents)
4. [Data Extraction & Storage](#data-extraction--storage)
5. [Advanced Usage](#advanced-usage)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)

## Core Concepts

### The GroupDiscussion Base Class

The `GroupDiscussion` class is the foundation of the framework. It handles:
- Agent initialization and management
- Discussion flow control
- Result extraction and storage
- Metadata management

```python
from group_discussion import GroupDiscussion, DiscussionType

discussion = GroupDiscussion(
    discussion_name="My Discussion",
    discussion_type=DiscussionType.FOCUS_GROUP,
    context="Context for the discussion"
)
```

### Basic Configuration

Every discussion requires:
1. A name
2. A discussion type
3. A situation or context
4. An extraction configuration

```python
discussion.set_situation("Description of the discussion situation")
discussion.configure_extraction(
    objective="What to extract from the discussion",
    fields=["field1", "field2"]
)
```

## Discussion Types

### 1. Focus Groups (ApartmentAdDiscussion)

Ideal for gathering collective feedback and ideas.

```python
from group_discussion import ApartmentAdDiscussion

discussion = ApartmentAdDiscussion("""
    Modern apartment with:
    - 2 bedrooms
    - Central location
    - Recent renovations
""")
results = discussion.run_discussion()
```

### 2. Product Brainstorming (ProductBrainstormingDiscussion)

Perfect for feature ideation and product development.

```python
from group_discussion import ProductBrainstormingDiscussion

discussion = ProductBrainstormingDiscussion(
    product_name="Mobile App",
    industry="healthcare"
)
results = discussion.run_discussion(num_steps=4)
```

### 3. Customer Interviews (CustomerInterviewDiscussion)

For in-depth customer research and feedback.

```python
from group_discussion import CustomerInterviewDiscussion

discussion = CustomerInterviewDiscussion(
    company_context="SaaS company in growth phase",
    customer_profile="Enterprise CTO with 15 years experience"
)
results = discussion.run_discussion(num_steps=5)
```

### 4. Ad Evaluation (AdEvaluationDiscussion)

For comparing and analyzing advertisements.

```python
from group_discussion import AdEvaluationDiscussion

ads = [
    "First ad content...",
    "Second ad content..."
]
discussion = AdEvaluationDiscussion("Software Product", ads)
results = discussion.run_discussion(reduce_results=True)
```

## Working with Agents

### Default Agents

The framework comes with pre-configured expert agents:
- Lisa (Data Scientist)
- Oscar (Architect)
- Marcos (Physician)

### Custom Agents

Create custom agents for specific needs:

```python
from tinytroupe.factory import TinyPersonFactory

factory = TinyPersonFactory("Company context")
custom_agent = factory.generate_person("""
    Senior marketing executive with 10 years
    experience in digital advertising
""")

discussion = GroupDiscussion(
    "Custom Discussion",
    DiscussionType.CUSTOM,
    agents=[custom_agent]
)
```

## Data Extraction & Storage

### Configuring Extraction

```python
discussion.configure_extraction(
    objective="Extract key insights about product features",
    fields=["features", "benefits", "drawbacks"],
    rapporteur_name="Lisa"  # Optional: specific agent for summarizing
)
```

### Storage Options

1. **File Storage**
```python
discussion.save_results(results, "path/to/output.json")
```

2. **Database Storage**
```python
# Automatically handled when saving results
# Configure in .env:
# DB_HOST=localhost
# DB_USER=user
# DB_PASSWORD=pass
# DB_NAME=dbname
```

## Advanced Usage

### 1. Adding Custom Context

```python
discussion.add_context("market_segment", "enterprise")
discussion.add_context("budget_range", "premium")
```

### 2. Result Reduction

Combine insights from multiple agents:

```python
results = discussion.run_discussion(reduce_results=True)
```

### 3. Custom Discussion Types

Create your own discussion type:

```python
class MarketResearchDiscussion(GroupDiscussion):
    def __init__(self, market_segment, competitors):
        super().__init__(
            f"{market_segment} Market Research",
            DiscussionType.CUSTOM
        )
        self.add_context("segment", market_segment)
        self.add_context("competitors", competitors)
        
        # Configure specific extraction
        self.configure_extraction(
            objective="Analyze market opportunities and threats",
            fields=["opportunities", "threats", "recommendations"]
        )
```

## Examples

### 1. Product Feature Evaluation

```python
from group_discussion import ProductBrainstormingDiscussion

# Evaluate new features for a text editor
discussion = ProductBrainstormingDiscussion(
    "Text Editor",
    "software development"
)

# Add specific context
discussion.add_context("target_users", "developers")
discussion.add_context("current_features", ["syntax highlighting", "auto-complete"])

# Run with more steps for deeper discussion
results = discussion.run_discussion(num_steps=5)
discussion.save_results(results, "feature_evaluation.json")
```

### 2. Customer Interview Series

```python
from group_discussion import CustomerInterviewDiscussion

# Interview different customer segments
segments = [
    ("Enterprise", "CTO with cloud migration needs"),
    ("Startup", "Technical founder focusing on rapid deployment"),
    ("SMB", "IT Manager handling hybrid infrastructure")
]

for segment, profile in segments:
    discussion = CustomerInterviewDiscussion(
        f"Cloud Services Provider - {segment} Segment",
        profile
    )
    results = discussion.run_discussion()
    discussion.save_results(
        results,
        f"interviews/{segment.lower()}_insights.json"
    )
```

## Troubleshooting

### Common Issues

1. **Agent Not Found**
   ```python
   # Solution: Check agent name or use default agents
   discussion.configure_extraction(rapporteur_name="Lisa")
   ```

2. **Database Connection**
   ```python
   # Check .env configuration and database availability
   # Ensure all required tables are created
   ```

3. **Extraction Fields Missing**
   ```python
   # Ensure fields match expected output
   discussion.configure_extraction(
       fields=["specific_field_name"]
   )
   ```

### Best Practices

1. **Discussion Steps**
   - Start with 3-4 steps for basic discussions
   - Use more steps (5-6) for complex topics
   - Monitor discussion quality vs. length

2. **Context Setting**
   - Provide clear, detailed situations
   - Include relevant background information
   - Specify desired outcomes

3. **Data Management**
   - Use consistent file naming
   - Include timestamps in filenames
   - Regular database backups

4. **Agent Selection**
   - Match agent expertise to discussion topic
   - Use custom agents for specialized knowledge
   - Consider agent interactions
