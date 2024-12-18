# TinyTroupe Analytics Documentation

## Overview
The TinyTroupe analytics system provides real-time insights into character interactions and discussion dynamics. This document details the analytics features, their implementation, and usage.

## Components

### 1. Data Collection
The analytics system collects data through the `ChatInterface` class, which tracks:
- Message content and timestamps
- Sender information
- Reactions and interactions
- Topic keywords
- Sentiment indicators

### 2. Analytics Dashboard
The dashboard is implemented in Streamlit and consists of four main sections:

#### a. Participation Overview
- **Total Messages**: Count of all messages in the discussion
- **Active Users**: Number of unique participants
- **Message Distribution**: Bar chart showing message count per character
- **Average Reactions**: Mean number of reactions per message

#### b. Sentiment Analysis
- Tracks emotional tone over time
- Uses a simple sentiment classifier (positive/negative)
- Visualizes sentiment trends in line charts

#### c. Topic Evolution
- Extracts key terms from messages
- Groups terms by time windows
- Shows topic progression with sentiment context
- Displays in an interactive data table

#### d. Interaction Network
- Creates a heatmap of character interactions
- Shows communication patterns
- Indicates relationship strengths
- Uses Plotly for interactive visualization

## Implementation Details

### Analytics Data Structure
```python
{
    "total_messages": int,
    "active_users": int,
    "messages_per_user": Dict[str, int],
    "reactions_per_message": List[int],
    "interaction_patterns": {
        "interaction_matrix": Dict[str, Dict[str, int]]
    },
    "topic_evolution": {
        "windows": List[Dict[str, Any]]
    }
}
```

### Key Methods
1. `ChatInterface.get_analytics()`: Generates analytics data
2. `render_analytics_dashboard()`: Creates Streamlit visualization
3. `analyze_sentiment()`: Processes message sentiment

## Usage Examples

### Basic Usage
```python
# In your Streamlit app
if st.sidebar.checkbox("Show Analytics"):
    render_analytics_dashboard()
```

### Accessing Analytics Data
```python
# Get raw analytics data
analytics = chat_interface.get_analytics()

# Access specific metrics
total_msgs = analytics["total_messages"]
active_users = analytics["active_users"]
```

## Best Practices
1. **Performance**: Analytics are computed on-demand to minimize overhead
2. **Visualization**: Use appropriate chart types for different metrics
3. **Updates**: Dashboard refreshes automatically with new messages
4. **Error Handling**: Gracefully handles missing or incomplete data

## Future Enhancements
- Advanced sentiment analysis using ML models
- More detailed interaction patterns
- Custom time window selection
- Export capabilities for analytics data
- Comparative analytics between discussions
