"""
Streamlit frontend for the chat interface and analytics.
"""
import os
import sys
from pathlib import Path
import json
from datetime import datetime, timedelta

# Determine the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List
import altair as alt
from textblob import TextBlob
from group_cases.src.tools.chat_interface import ChatInterface, MessageType
from enhanced_group_memory.src.core.characters import (
    Character, 
    CharacterGroup,
    create_lisa_the_data_scientist,
    create_oscar_the_architect
)
from enhanced_group_memory.src.core.discussion import (
    GroupDiscussion,
    DiscussionType
)

def init_session_state():
    """Initialize session state variables."""
    if 'discussion' not in st.session_state:
        st.session_state.discussion = None
    if 'chat_interface' not in st.session_state:
        st.session_state.chat_interface = ChatInterface()
    if 'current_user' not in st.session_state:
        st.session_state.current_user = "User"
    if 'show_analytics' not in st.session_state:
        st.session_state.show_analytics = False
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    if 'discussion_started' not in st.session_state:
        st.session_state.discussion_started = False
    if 'sentiment_history' not in st.session_state:
        st.session_state.sentiment_history = []
    if 'selected_characters' not in st.session_state:
        st.session_state.selected_characters = []
    if 'character_group' not in st.session_state:
        st.session_state.character_group = None
    if 'discussion_obj' not in st.session_state:
        st.session_state.discussion_obj = None
    
    # Initialize available characters
    if 'character_creators' not in st.session_state:
        st.session_state.character_creators = {
            'Lisa': create_lisa_the_data_scientist,
            'Oscar': create_oscar_the_architect
        }
    
    # Initialize scenarios
    if 'scenarios' not in st.session_state:
        st.session_state.scenarios = {
            'Data Architecture': {
                'topic': 'Designing Data-Driven Architecture',
                'prompt': 'How can we integrate data analytics into architectural design to create smarter buildings?'
            },
            'Smart Cities': {
                'topic': 'Future of Smart Cities',
                'prompt': 'What role should data analysis play in urban development and city planning?'
            }
        }

def analyze_sentiment(text: str) -> float:
    """Analyze sentiment of text using TextBlob."""
    blob = TextBlob(text)
    return blob.sentiment.polarity

def render_message(message: Any):
    """Render a chat message."""
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write(f"**{message.sender}**")
            st.caption(message.timestamp.strftime("%H:%M:%S"))
        with col2:
            st.markdown(message.content)
            sentiment = analyze_sentiment(message.content)
            sentiment_color = "🟢" if sentiment > 0 else "🔴" if sentiment < 0 else "⚪"
            st.caption(f"Sentiment: {sentiment_color} ({sentiment:.2f})")
            if message.reactions:
                reaction_text = " | ".join(
                    [f"{r} ({len(users)})" for r, users in message.reactions.items()]
                )
                st.caption(f"Reactions: {reaction_text}")

def render_results():
    """Render discussion results."""
    if not st.session_state.discussion:
        return
    
    st.subheader("Discussion Results")
    results = st.session_state.discussion.get_results()
    if results:
        # Create tabs for different result views
        result_tabs = st.tabs(["Summary", "Raw Data", "Export"])
        
        with result_tabs[0]:
            st.markdown("### Key Points")
            for key, value in results.items():
                st.markdown(f"**{key}:**")
                if isinstance(value, list):
                    for item in value:
                        st.markdown(f"- {item}")
                else:
                    st.markdown(value)
        
        with result_tabs[1]:
            st.json(results)
        
        with result_tabs[2]:
            st.download_button(
                "Download Results (JSON)",
                data=json.dumps(results, indent=2),
                file_name=f"discussion_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def render_analytics_dashboard():
    """Render analytics dashboard."""
    if not st.session_state.discussion_obj:
        st.warning("Start a discussion to see analytics.")
        return
        
    analytics = st.session_state.discussion_obj.chat_interface.get_analytics()
    
    # Create tabs for different analytics views
    analytics_tabs = st.tabs(["Overview", "Sentiment Analysis", "Topic Evolution", "Interaction Network"])
    
    with analytics_tabs[0]:
        st.subheader("Participation Overview")
        
        # Display participation metrics in a grid
        metrics_cols = st.columns(2)
        with metrics_cols[0]:
            st.metric("Total Messages", analytics.get("total_messages", 0))
        with metrics_cols[1]:
            st.metric("Active Users", analytics.get("active_users", 0))
        if analytics.get("reactions_per_message"):
            avg_reactions = sum(analytics["reactions_per_message"]) / len(analytics["reactions_per_message"])
            st.metric("Avg Reactions", f"{avg_reactions:.2f}")
        else:
            st.metric("Avg Reactions", "0")
        
        # Convert participation data to DataFrame
        messages_per_user = analytics.get("messages_per_user", {})
        if messages_per_user:
            participation_df = pd.DataFrame([
                {"User": user, "Messages": count}
                for user, count in messages_per_user.items()
            ])
            st.bar_chart(participation_df.set_index("User"))
        else:
            st.info("No messages yet.")
    
    with analytics_tabs[1]:
        st.subheader("Sentiment Analysis")
        topic_evolution = analytics.get("topic_evolution", {}).get("windows", [])
        if topic_evolution:
            sentiment_df = pd.DataFrame([
                {
                    "Time": window["timestamp_start"],
                    "Sentiment": 1 if window["sentiment"] == "positive" else -1
                }
                for window in topic_evolution
            ])
            if not sentiment_df.empty:
                st.line_chart(sentiment_df.set_index("Time"))
        else:
            st.info("Not enough messages for sentiment analysis.")
    
    with analytics_tabs[2]:
        st.subheader("Topic Evolution")
        topic_evolution = analytics.get("topic_evolution", {}).get("windows", [])
        if topic_evolution:
            topic_df = pd.DataFrame([
                {
                    "Time": window["timestamp_start"],
                    "Topics": ", ".join(list(window["key_terms"].keys())[:3]),
                    "Sentiment": window["sentiment"]
                }
                for window in topic_evolution
            ])
            
            if not topic_df.empty:
                st.dataframe(topic_df)
        else:
            st.info("Not enough messages for topic analysis.")
    
    with analytics_tabs[3]:
        st.subheader("Interaction Network")
        interactions = analytics.get("interaction_patterns", {}).get("interaction_matrix", {})
        if interactions and len(interactions) > 1:  # Need at least 2 users for interactions
            interaction_df = pd.DataFrame([
                {
                    "From": user1,
                    "To": user2,
                    "Count": count
                }
                for user1, targets in interactions.items()
                for user2, count in targets.items()
            ])
            
            if not interaction_df.empty:
                # Create a heatmap of interactions
                pivot_df = interaction_df.pivot(index="From", columns="To", values="Count").fillna(0)
                fig = px.imshow(
                    pivot_df,
                    labels=dict(x="To", y="From", color="Interactions"),
                    title="Interaction Heatmap"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough interactions to display network.")

def main():
    """Main Streamlit app."""
    st.title("Enhanced Group Discussion")
    init_session_state()

    # Character selection
    st.sidebar.header("Select Characters")
    
    # Create character instances with unique IDs
    available_characters = st.session_state.character_creators
    
    # Store original names for display
    display_names = {}
    character_info = {}
    
    # Create characters once to get their full names and info
    for short_name, creator_func in available_characters.items():
        character = creator_func()
        display_names[character.name] = short_name
        character_info[character.name] = character.occupation
    
    selected_chars = st.sidebar.multiselect(
        "Choose characters for the discussion:",
        options=list(available_characters.keys()),
        default=[]
    )
    
    # Update selected characters
    st.session_state.selected_characters = [
        available_characters[char_name]() for char_name in selected_chars
    ]
    
    # Discussion topic and start button
    st.sidebar.header("Discussion")
    if 'topic' not in st.session_state:
        st.session_state.topic = ""
    if 'discussion_obj' not in st.session_state:
        st.session_state.discussion_obj = None
        
    scenario = st.sidebar.selectbox("Select a scenario", list(st.session_state.scenarios.keys()))
    topic = st.session_state.scenarios[scenario]["topic"]
    initial_prompt = st.session_state.scenarios[scenario]["prompt"]
    
    if st.sidebar.button("Start Discussion") and len(selected_chars) > 0 and topic and initial_prompt:
        # Create character group and discussion object
        st.session_state.character_group = CharacterGroup(st.session_state.selected_characters)
        st.session_state.topic = topic
        
        # Create a discussion object with the proper type and context
        st.session_state.discussion_obj = GroupDiscussion(
            discussion_name=topic,
            discussion_type=DiscussionType.CUSTOM,
            context=initial_prompt
        )
        
        # Add the initial prompt as a system message
        st.session_state.discussion_obj.chat_interface.add_message(
            sender="System",
            content=initial_prompt,
            msg_type=MessageType.SYSTEM
        )
        
        st.session_state.discussion_started = True
        st.experimental_rerun()
    
    # Show discussion area if started
    if st.session_state.discussion_started and st.session_state.character_group:
        st.subheader(f"Discussion: {st.session_state.topic}")
        
        # Display messages from chat history
        for message in st.session_state.discussion_obj.chat_interface.messages:
            sender = message.sender
            if sender in display_names:
                sender = display_names[sender]
            with st.chat_message(sender.lower()):
                if sender in display_names:
                    st.write(f"**{sender}** ({character_info[sender]}):")
                st.write(message.content)
        
        # Add continue button
        continue_chat = st.button("Continue Discussion")
        
        # Add user input
        user_input = st.chat_input("Your message")
        
        if continue_chat:
            # Generate a continuation prompt based on the discussion context
            last_messages = st.session_state.discussion_obj.chat_interface.messages[-3:]
            context = "\n".join([f"{msg.sender}: {msg.content}" for msg in last_messages])
            continuation_prompt = f"Based on the recent discussion:\n{context}\n\nPlease continue the conversation."
            
            # Get responses from characters
            for char in st.session_state.selected_characters:
                response = st.session_state.character_group._generate_character_response(
                    char, 
                    continuation_prompt,
                    st.session_state.discussion_obj
                )
                
                display_name = display_names.get(char.name, char.name)
                with st.chat_message(display_name.lower()):
                    st.write(f"**{display_name}** ({char.occupation}):")
                    if response:
                        st.write(response)
                        # Add character response to discussion
                        st.session_state.discussion_obj.chat_interface.add_message(
                            sender=char.name,
                            content=response,
                            msg_type=MessageType.TEXT
                        )
                    else:
                        st.error("No response generated")
            
            st.experimental_rerun()
        
        if user_input:
            # Add user message to discussion
            st.session_state.discussion_obj.chat_interface.add_message(
                sender="User",
                content=user_input,
                msg_type=MessageType.TEXT
            )
            
            # Display user message
            with st.chat_message("user"):
                st.write(user_input)
            
            # Get responses from characters
            for char in st.session_state.selected_characters:
                response = st.session_state.character_group._generate_character_response(
                    char, 
                    user_input,
                    st.session_state.discussion_obj
                )
                
                display_name = display_names.get(char.name, char.name)
                with st.chat_message(display_name.lower()):
                    st.write(f"**{display_name}** ({char.occupation}):")
                    if response:
                        st.write(response)
                        # Add character response to discussion
                        st.session_state.discussion_obj.chat_interface.add_message(
                            sender=char.name,
                            content=response,
                            msg_type=MessageType.TEXT
                        )
                    else:
                        st.error("No response generated")
                
                # Optional: Show character's recent memory for debugging
                if st.sidebar.checkbox("Show Character Memory", key=f"show_memory_{char.name}"):
                    with st.expander(f"{char.name}'s Recent Memory"):
                        recent_memory = char.tiny_person.episodic_memory.retrieve_recent()
                        for memory in recent_memory:
                            st.write(memory)
    
    # Show analytics if discussion has started
    if st.session_state.discussion_started:
        if st.sidebar.checkbox("Show Analytics"):
            render_analytics_dashboard()

if __name__ == "__main__":
    main()
