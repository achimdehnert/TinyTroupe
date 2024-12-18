"""
Main Streamlit application that combines group discussions with enhanced memory capabilities.
"""
import os
import sys
from datetime import datetime
import json
from typing import Dict, Any
import pandas as pd

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

import streamlit as st
from enhanced_group_memory.src.core.discussion import (
    GroupDiscussion,
    ApartmentAdDiscussion,
    ProductBrainstormingDiscussion,
    CustomerInterviewDiscussion,
    AdEvaluationDiscussion,
    MessageType
)
from enhanced_group_memory.src.core.analytics import DiscussionAnalytics
from enhanced_group_memory.src.utils.config import Config
from enhanced_group_memory.src.core.characters import (
    Character, CharacterGroup,
    create_lisa_the_data_scientist,
    create_oscar_the_architect
)

def init_session_state():
    """Initialize session state variables."""
    if 'current_discussion' not in st.session_state:
        st.session_state.current_discussion = None
    if 'all_characters' not in st.session_state:
        # Initialize all available characters
        st.session_state.all_characters = {
            'Lisa_DS': create_lisa_the_data_scientist(),
            'Oscar_Arch': create_oscar_the_architect(),
            'Emma_UX': Character(
                name="Emma_UX",
                age=25,
                occupation="UX Designer",
                nationality="Swedish",
                interests=["User Research", "Design Systems", "Psychology", "Art"],
                personality=["Empathetic", "Observant", "Creative", "Organized"]
            ),
            'Marcus_Dev': Character(
                name="Marcus_Dev",
                age=32,
                occupation="Product Manager",
                nationality="German",
                interests=["Market Analysis", "Team Leadership", "Technology Trends", "Rock Climbing"],
                personality=["Strategic", "Decisive", "Communicative", "Adaptable"]
            ),
            'Sophia_ES': Character(
                name="Sophia_ES",
                age=29,
                occupation="Environmental Scientist",
                nationality="Brazilian",
                interests=["Climate Change", "Biodiversity", "Data Analysis", "Yoga"],
                personality=["Analytical", "Passionate", "Detail-oriented", "Collaborative"]
            )
        }
    if 'selected_characters' not in st.session_state:
        st.session_state.selected_characters = []
    if 'character_group' not in st.session_state:
        st.session_state.character_group = None
    if 'discussion_topic' not in st.session_state:
        st.session_state.discussion_topic = ""
    if 'discussion_prompt' not in st.session_state:
        st.session_state.discussion_prompt = ""
    if 'discussion_output' not in st.session_state:
        st.session_state.discussion_output = []

def render_sidebar():
    """Render the sidebar with settings and controls."""
    with st.sidebar:
        st.title("Settings ⚙️")
        
        # Discussion type selection
        if not st.session_state.current_discussion:
            discussion_type = st.selectbox(
                "Select Discussion Type",
                [
                    "Apartment Ad Creation",
                    "Product Feature Brainstorming",
                    "Customer Interview",
                    "Ad Evaluation"
                ]
            )
            
            # Discussion-specific inputs
            if discussion_type == "Apartment Ad Creation":
                with st.expander("Configure Discussion", expanded=True):
                    apartment_desc = st.text_area(
                        "Apartment Description",
                        "A modern 2-bedroom apartment in downtown..."
                    )
                    if st.button("Start Discussion", type="primary"):
                        st.session_state.discussion = ApartmentAdDiscussion(apartment_desc)
                        st.session_state.current_discussion = st.session_state.discussion
                        st.rerun()
                    
            elif discussion_type == "Product Feature Brainstorming":
                with st.expander("Configure Discussion", expanded=True):
                    product_name = st.text_input("Product Name", "MyProduct")
                    industry = st.text_input("Industry", "Technology")
                    if st.button("Start Discussion", type="primary"):
                        st.session_state.discussion = ProductBrainstormingDiscussion(product_name, industry)
                        st.session_state.current_discussion = st.session_state.discussion
                        st.rerun()
                    
            elif discussion_type == "Customer Interview":
                with st.expander("Configure Discussion", expanded=True):
                    company_context = st.text_area(
                        "Company Context",
                        "We are a software company..."
                    )
                    customer_profile = st.text_area(
                        "Customer Profile",
                        "A senior manager in a large enterprise..."
                    )
                    if st.button("Start Discussion", type="primary"):
                        st.session_state.discussion = CustomerInterviewDiscussion(company_context, customer_profile)
                        st.session_state.current_discussion = st.session_state.discussion
                        st.rerun()
                    
            elif discussion_type == "Ad Evaluation":
                with st.expander("Configure Discussion", expanded=True):
                    product_type = st.text_input("Product Type", "Software")
                    num_ads = st.number_input("Number of Ads", min_value=1, max_value=5, value=2)
                    ads = []
                    for i in range(num_ads):
                        ad = st.text_area(f"Ad {i+1}", f"Sample ad {i+1}")
                        ads.append(ad)
                    if st.button("Start Discussion", type="primary"):
                        st.session_state.discussion = AdEvaluationDiscussion(product_type, ads)
                        st.session_state.current_discussion = st.session_state.discussion
                        st.rerun()
        
        # Controls for started discussion
        if st.session_state.current_discussion:
            st.session_state.current_user = st.text_input(
                "Your Name",
                value="User"
            )
            
            st.session_state.show_analytics = st.checkbox(
                "Show Analytics",
                value=True
            )
            
            st.session_state.show_memory = st.checkbox(
                "Show Memory System",
                value=True
            )
            
            if st.button("Reset Discussion", type="secondary"):
                st.session_state.discussion = None
                st.session_state.current_discussion = None
                st.session_state.sentiment_history = []
                st.rerun()

def render_discussion_tab():
    """Render the discussion tab."""
    chat_container = st.container()
    with chat_container:
        messages = st.session_state.discussion.chat_interface.messages
        for message in messages:
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.write(f"**{message.sender}**")
                    st.caption(message.timestamp.strftime("%H:%M:%S"))
                with col2:
                    st.markdown(message.content)
                    sentiment = DiscussionAnalytics.analyze_sentiment(message.content)
                    sentiment_color = "🟢" if sentiment > 0 else "🔴" if sentiment < 0 else "⚪"
                    st.caption(f"Sentiment: {sentiment_color} ({sentiment:.2f})")
                    if message.reactions:
                        reaction_text = " | ".join(
                            [f"{r} ({len(users)})" for r, users in message.reactions.items()]
                        )
                        st.caption(f"Reactions: {reaction_text}")
    
    # Message input
    with st.container():
        message = st.text_area("Message", height=100)
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("Send 📤", type="primary") and message.strip():
                # Add message
                st.session_state.discussion.add_message(
                    st.session_state.current_user,
                    message
                )
                
                # Update sentiment history
                sentiment = DiscussionAnalytics.analyze_sentiment(message)
                if 'sentiment_history' not in st.session_state:
                    st.session_state.sentiment_history = []
                st.session_state.sentiment_history.append({
                    'timestamp': datetime.now(),
                    'sentiment': sentiment
                })
                
                st.rerun()

def render_memory_tab():
    """Render the memory system tab."""
    st.subheader("Memory System")
    
    # Memory search
    search_query = st.text_input("Search Memories", placeholder="Enter search query...")
    if search_query:
        memories = st.session_state.discussion.search_discussion(search_query)
        if memories:
            st.write(f"Found {len(memories)} relevant memories:")
            for memory in memories:
                with st.expander(f"Memory from {memory.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"):
                    st.write(memory.content)
                    st.json(memory.context)
        else:
            st.info("No relevant memories found.")
    
    # Memory consolidation
    if st.button("Consolidate Memories"):
        consolidated = st.session_state.discussion.consolidate_memories()
        if consolidated:
            st.success(f"Consolidated {len(consolidated)} memories!")
            for memory in consolidated:
                with st.expander(f"Consolidated Memory"):
                    st.write(memory.content)
                    st.json(memory.context)
        else:
            st.info("No memories to consolidate at this time.")

def render_analytics_tab():
    """Render the analytics tab."""
    analytics = st.session_state.discussion.get_analytics()
    
    # Create tabs for different analytics views
    analytics_tabs = st.tabs(["Overview", "Sentiment", "Topics", "Interactions"])
    
    with analytics_tabs[0]:
        st.subheader("Discussion Overview")
        
        # Display metrics in a grid
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", analytics["total_messages"])
        with col2:
            st.metric("Active Users", analytics["active_users"])
        with col3:
            st.metric("Avg. Sentiment", sum(st.session_state.sentiment_history) / len(st.session_state.sentiment_history) if st.session_state.sentiment_history else 0)
        with col4:
            st.metric("Topics Discussed", len(analytics.get("topic_evolution", {}).get("windows", [])))
    
    with analytics_tabs[1]:
        st.subheader("Sentiment Analysis")
        if st.session_state.sentiment_history:
            sentiment_data = pd.DataFrame(st.session_state.sentiment_history)
            st.line_chart(sentiment_data.set_index('timestamp'))
    
    with analytics_tabs[2]:
        st.subheader("Topic Evolution")
        topic_evolution = analytics.get("topic_evolution", {}).get("windows", [])
        if topic_evolution:
            for window in topic_evolution:
                st.write(f"Time: {window['timestamp_start']} - {window.get('timestamp_end', 'now')}")
                st.write("Key Terms:", ", ".join(window["key_terms"].keys()))
    
    with analytics_tabs[3]:
        st.subheader("Interaction Patterns")
        interactions = analytics.get("interaction_patterns", {}).get("interaction_matrix", {})
        if interactions:
            st.json(interactions)

def render_character_interaction_tab():
    """Render the character interaction tab."""
    st.subheader("Character Selection and Discussion Setup")
    
    # Character selection
    st.write("Select characters for the discussion:")
    selected_chars = []
    cols = st.columns(3)
    for i, (name, char) in enumerate(st.session_state.all_characters.items()):
        with cols[i % 3]:
            if st.checkbox(f"{name} - {char.occupation}", key=f"char_{name}"):
                selected_chars.append(char)
    
    # Topic and prompt setup
    st.write("---")
    st.write("Configure the discussion:")
    topic = st.text_input("Discussion Topic", st.session_state.discussion_topic)
    prompt = st.text_area("Initial Prompt", st.session_state.discussion_prompt,
                         help="Set the context and initial direction for the discussion")
    
    # Start discussion button
    if st.button("Start Discussion", disabled=len(selected_chars) < 2):
        if len(selected_chars) < 2:
            st.warning("Please select at least 2 characters")
        else:
            st.session_state.selected_characters = selected_chars
            st.session_state.character_group = CharacterGroup(selected_chars)
            st.session_state.discussion_topic = topic
            st.session_state.discussion_prompt = prompt
            st.session_state.current_discussion = st.session_state.character_group.start_discussion(
                topic, prompt
            )
            st.session_state.discussion_output = []  # Reset output
            st.rerun()
    
    # Display current discussion
    if st.session_state.current_discussion is not None:
        st.write("---")
        
        # Create tabs for Discussion, Results, and Documentation
        disc_tab, results_tab, doc_tab = st.tabs(["Discussion", "Results", "Documentation"])
        
        with disc_tab:
            st.subheader("Current Discussion")
            # Display messages
            for msg in st.session_state.current_discussion.chat_interface.messages:
                with st.chat_message(msg.sender.lower()):
                    st.write(msg.content)
                    # Store for documentation
                    st.session_state.discussion_output.append({
                        'sender': msg.sender,
                        'content': msg.content,
                        'timestamp': str(msg.timestamp)
                    })
            
            # Generate responses button
            if st.button("Continue Discussion"):
                for char in st.session_state.selected_characters:
                    response = st.session_state.character_group.get_character_response(
                        char, st.session_state.current_discussion
                    )
                    st.session_state.current_discussion.chat_interface.add_message(
                        sender=char.name,
                        content=response
                    )
                st.rerun()
        
        with results_tab:
            st.subheader("Discussion Results")
            if st.session_state.character_group:
                results = st.session_state.character_group.get_discussion_summary()
                
                # Show participant statistics
                st.write("### Participant Contributions")
                for participant in results['participants']:
                    st.write(f"**{participant['name']}** ({participant['occupation']} from {participant['nationality']})")
                    st.write(f"- Contributions: {participant['contributions']}")
                
                # Show key points
                st.write("### Key Points")
                for point in results['key_points'][-5:]:  # Show last 5 points
                    st.write(f"- **{point['character']}:** {point['point']}")
                
                # Show insights
                st.write("### Character Insights")
                for insight in results['insights'][-3:]:  # Show last 3 insights
                    st.write(f"**{insight['character']}** ({insight['expertise']}):")
                    st.write(f"- {insight['insight']}")
                
                # Show sentiment analysis
                st.write("### Sentiment Analysis")
                sentiments = results['sentiment_analysis']
                if sentiments:
                    # Create a simple bar chart of sentiment counts
                    sentiment_counts = {}
                    for s in sentiments:
                        sentiment_counts[s['character']] = sentiment_counts.get(s['character'], {})
                        sentiment_counts[s['character']][s['sentiment']] = sentiment_counts[s['character']].get(s['sentiment'], 0) + 1
                    
                    # Convert to percentage
                    for char in sentiment_counts:
                        total = sum(sentiment_counts[char].values())
                        for sentiment in sentiment_counts[char]:
                            sentiment_counts[char][sentiment] = (sentiment_counts[char][sentiment] / total) * 100
                    
                    # Display as a table
                    st.write("Sentiment Distribution (%):")
                    sentiment_df = pd.DataFrame(sentiment_counts).fillna(0)
                    st.dataframe(sentiment_df)
        
        with doc_tab:
            st.subheader("Discussion Documentation")
            if st.button("Export Discussion"):
                export_discussion_to_markdown()
            
            # Preview documentation
            st.write("### Documentation Preview")
            st.write(f"**Topic:** {st.session_state.discussion_topic}")
            st.write(f"**Initial Prompt:** {st.session_state.discussion_prompt}")
            st.write("\n**Participants:**")
            for char in st.session_state.selected_characters:
                st.write(f"- {char.name} ({char.occupation} from {char.nationality})")
            
            st.write("\n**Discussion Highlights:**")
            if st.session_state.character_group:
                results = st.session_state.character_group.get_discussion_summary()
                for insight in results['insights'][-3:]:
                    st.write(f"- {insight['character']}: {insight['insight']}")

def export_discussion_to_markdown():
    """Export the current discussion to a markdown file."""
    if not st.session_state.discussion_output:
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"discussion_{timestamp}.md"
    filepath = os.path.join(os.path.dirname(__file__), '..', '..', 'outputs', filename)
    
    # Create outputs directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header
        f.write(f"# {st.session_state.discussion_topic}\n\n")
        f.write("## Discussion Setup\n\n")
        f.write(f"**Initial Prompt:** {st.session_state.discussion_prompt}\n\n")
        
        # Write participant information
        f.write("## Participants\n\n")
        for char in st.session_state.selected_characters:
            f.write(f"### {char.name}\n")
            f.write(f"- **Occupation:** {char.occupation}\n")
            f.write(f"- **Age:** {char.age}\n")
            f.write(f"- **Nationality:** {char.nationality}\n")
            f.write("- **Interests:**\n")
            for interest in char.interests:
                f.write(f"  - {interest}\n")
            f.write("- **Personality Traits:**\n")
            for trait in char.personality:
                f.write(f"  - {trait}\n")
            f.write("\n")
        
        # Write discussion
        f.write("## Discussion\n\n")
        for msg in st.session_state.discussion_output:
            f.write(f"**{msg['sender']}:** {msg['content']}\n\n")
    
    st.success(f"Discussion exported to {filename}")

def main():
    """Main Streamlit app."""
    # Set page config
    st.set_page_config(
        page_title=Config.APP_NAME,
        page_icon="💭",
        layout="wide"
    )
    
    # Initialize session state
    init_session_state()
    
    # Apply theme
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {Config.THEME["backgroundColor"]};
            color: {Config.THEME["textColor"]};
        }}
        </style>
    """, unsafe_allow_html=True)
    
    st.title(f"{Config.APP_NAME} 💬")
    
    # Character selection
    st.write("### Select Characters for Discussion")
    st.write("Choose at least 2 characters to start a discussion:")
    
    selected_chars = []
    cols = st.columns(3)
    for i, (name, char) in enumerate(st.session_state.all_characters.items()):
        with cols[i % 3]:
            with st.expander(f"{name} - {char.occupation}"):
                st.write(f"**Age:** {char.age}")
                st.write(f"**Nationality:** {char.nationality}")
                st.write("**Interests:**")
                for interest in char.interests:
                    st.write(f"- {interest}")
                st.write("**Personality:**")
                for trait in char.personality:
                    st.write(f"- {trait}")
                if st.checkbox("Select", key=f"char_{name}"):
                    selected_chars.append(char)
    
    # Topic and prompt setup
    st.write("---")
    st.write("### Configure Discussion")
    topic = st.text_input("Discussion Topic", st.session_state.discussion_topic,
                         placeholder="e.g., 'The Future of Sustainable Design'")
    prompt = st.text_area("Initial Prompt", st.session_state.discussion_prompt,
                         placeholder="e.g., 'Discuss how technology and design can promote environmental sustainability'",
                         help="Set the context and initial direction for the discussion")
    
    # Start discussion button
    if st.button("Start Discussion", disabled=len(selected_chars) < 2, type="primary"):
        if len(selected_chars) < 2:
            st.warning("Please select at least 2 characters")
        else:
            st.session_state.selected_characters = selected_chars
            st.session_state.character_group = CharacterGroup(selected_chars)
            st.session_state.discussion_topic = topic
            st.session_state.discussion_prompt = prompt
            st.session_state.current_discussion = st.session_state.character_group.start_discussion(
                topic, prompt
            )
            st.session_state.discussion_output = []  # Reset output
            st.rerun()
    
    # Display current discussion
    if st.session_state.current_discussion is not None:
        st.write("---")
        
        # Create tabs for Discussion, Results, and Documentation
        disc_tab, results_tab, doc_tab = st.tabs(["Discussion", "Results", "Documentation"])
        
        with disc_tab:
            st.subheader("Current Discussion")
            # Display messages
            for msg in st.session_state.current_discussion.chat_interface.messages:
                with st.chat_message(msg.sender.lower()):
                    st.write(msg.content)
                    # Store for documentation
                    st.session_state.discussion_output.append({
                        'sender': msg.sender,
                        'content': msg.content,
                        'timestamp': str(msg.timestamp)
                    })
            
            # Generate responses button
            if st.button("Continue Discussion", type="primary"):
                for char in st.session_state.selected_characters:
                    response = st.session_state.character_group.get_character_response(
                        char, st.session_state.current_discussion
                    )
                    st.session_state.current_discussion.chat_interface.add_message(
                        sender=char.name,
                        content=response
                    )
                st.rerun()
        
        with results_tab:
            st.subheader("Discussion Results")
            if st.session_state.character_group:
                results = st.session_state.character_group.get_discussion_summary()
                
                # Show participant statistics
                st.write("### Participant Contributions")
                for participant in results['participants']:
                    st.write(f"**{participant['name']}** ({participant['occupation']} from {participant['nationality']})")
                    st.write(f"- Contributions: {participant['contributions']}")
                
                # Show key points
                st.write("### Key Points")
                for point in results['key_points'][-5:]:  # Show last 5 points
                    st.write(f"- **{point['character']}:** {point['point']}")
                
                # Show insights
                st.write("### Character Insights")
                for insight in results['insights'][-3:]:  # Show last 3 insights
                    st.write(f"**{insight['character']}** ({insight['expertise']}):")
                    st.write(f"- {insight['insight']}")
                
                # Show sentiment analysis
                st.write("### Sentiment Analysis")
                sentiments = results['sentiment_analysis']
                if sentiments:
                    # Create a simple bar chart of sentiment counts
                    sentiment_counts = {}
                    for s in sentiments:
                        sentiment_counts[s['character']] = sentiment_counts.get(s['character'], {})
                        sentiment_counts[s['character']][s['sentiment']] = sentiment_counts[s['character']].get(s['sentiment'], 0) + 1
                    
                    # Convert to percentage
                    for char in sentiment_counts:
                        total = sum(sentiment_counts[char].values())
                        for sentiment in sentiment_counts[char]:
                            sentiment_counts[char][sentiment] = (sentiment_counts[char][sentiment] / total) * 100
                    
                    # Display as a table
                    st.write("Sentiment Distribution (%):")
                    sentiment_df = pd.DataFrame(sentiment_counts).fillna(0)
                    st.dataframe(sentiment_df)
        
        with doc_tab:
            st.subheader("Discussion Documentation")
            if st.button("Export Discussion"):
                export_discussion_to_markdown()
            
            # Preview documentation
            st.write("### Documentation Preview")
            st.write(f"**Topic:** {st.session_state.discussion_topic}")
            st.write(f"**Initial Prompt:** {st.session_state.discussion_prompt}")
            st.write("\n**Participants:**")
            for char in st.session_state.selected_characters:
                st.write(f"- {char.name} ({char.occupation} from {char.nationality})")
            
            st.write("\n**Discussion Highlights:**")
            if st.session_state.character_group:
                results = st.session_state.character_group.get_discussion_summary()
                for insight in results['insights'][-3:]:
                    st.write(f"- {insight['character']}: {insight['insight']}")

if __name__ == "__main__":
    main()
