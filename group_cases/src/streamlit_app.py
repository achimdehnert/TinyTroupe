"""
Streamlit frontend for the chat interface and analytics.
"""
import os
import sys
from pathlib import Path

# Determine the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, Any, List
import altair as alt
from TinyTroupe.group_cases.src.tools.chat_interface import ChatInterface, MessageType
from TinyTroupe.group_cases.src.tools.advanced_analytics import DiscussionAnalytics

def init_session_state():
    """Initialize session state variables."""
    if 'chat_interface' not in st.session_state:
        st.session_state.chat_interface = ChatInterface()
    if 'current_user' not in st.session_state:
        st.session_state.current_user = "User"
    if 'current_thread' not in st.session_state:
        st.session_state.current_thread = None
    if 'show_analytics' not in st.session_state:
        st.session_state.show_analytics = False

def render_message(message: Any):
    """Render a chat message."""
    with st.container():
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.write(f"**{message.sender}**")
            st.caption(message.timestamp.strftime("%H:%M:%S"))
            
        with col2:
            message_container = st.container()
            with message_container:
                st.markdown(message.content)
                
                if message.reactions:
                    reaction_text = " | ".join(
                        [f"{r} ({len(users)})" for r, users in message.reactions.items()]
                    )
                    st.caption(f"Reactions: {reaction_text}")
                    
                if message.thread_id:
                    st.caption(f"Thread: {message.thread_id}")

def render_analytics_dashboard():
    """Render analytics dashboard."""
    analytics = st.session_state.chat_interface.get_analytics()
    
    # Participation Overview
    st.subheader("Participation Overview")
    participation = analytics["participation_metrics"]
    
    # Convert participation data to DataFrame
    participation_df = pd.DataFrame([
        {
            "User": user,
            "Messages": data["message_count"],
            "Avg Words": data["avg_message_length"],
            "Response Time": data.get("avg_response_time", 0)
        }
        for user, data in participation.items()
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            participation_df,
            x="User",
            y="Messages",
            title="Message Count by User"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        fig = px.scatter(
            participation_df,
            x="Messages",
            y="Avg Words",
            text="User",
            title="Message Count vs Average Length"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    # Topic Evolution
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
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=topic_df["Time"],
            y=topic_df["Sentiment"],
            mode='lines+markers',
            name='Sentiment'
        ))
        fig.update_layout(title="Topic Evolution and Sentiment")
        st.plotly_chart(fig, use_container_width=True)
        
        st.table(topic_df)
        
    # Interaction Network
    st.subheader("Interaction Network")
    interactions = analytics.get("interaction_patterns", {}).get("interaction_matrix", {})
    if interactions:
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
            fig = px.scatter(
                interaction_df,
                x="From",
                y="To",
                size="Count",
                title="Interaction Network"
            )
            st.plotly_chart(fig, use_container_width=True)

def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="Chat Analytics Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("Chat Settings")
        st.session_state.current_user = st.text_input(
            "Your Name",
            value=st.session_state.current_user
        )
        
        # Thread selection
        threads = list(st.session_state.chat_interface.threads.keys())
        if threads:
            st.session_state.current_thread = st.selectbox(
                "Select Thread",
                ["None"] + threads
            )
            if st.session_state.current_thread == "None":
                st.session_state.current_thread = None
                
        # Toggle analytics
        st.session_state.show_analytics = st.checkbox(
            "Show Analytics",
            value=st.session_state.show_analytics
        )
        
        # Export options
        if st.button("Export Chat"):
            export_format = st.radio(
                "Export Format",
                ["json", "markdown", "html"]
            )
            exported = st.session_state.chat_interface.export_chat_history(
                format=export_format,
                include_analytics=True
            )
            st.download_button(
                "Download Export",
                exported,
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format}",
                mime="text/plain"
            )
    
    # Main chat area
    st.title("Chat Interface")
    
    # Message input
    with st.container():
        message = st.text_area("Message", height=100)
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("Send"):
                if message.strip():
                    st.session_state.chat_interface.add_message(
                        sender=st.session_state.current_user,
                        content=message,
                        thread_id=st.session_state.current_thread
                    )
                    st.experimental_rerun()
                    
        with col2:
            msg_type = st.selectbox(
                "Message Type",
                [t.value for t in MessageType]
            )
            
        with col3:
            if st.button("Create Thread"):
                if len(st.session_state.chat_interface.messages) > 0:
                    thread_id = st.session_state.chat_interface.create_thread(
                        len(st.session_state.chat_interface.messages) - 1
                    )
                    if thread_id:
                        st.session_state.current_thread = thread_id
                        st.experimental_rerun()
    
    # Chat history
    st.subheader("Chat History")
    messages = (
        st.session_state.chat_interface.get_thread_messages(st.session_state.current_thread)
        if st.session_state.current_thread
        else st.session_state.chat_interface.messages
    )
    
    for msg in messages:
        render_message(msg)
        
    # Analytics dashboard
    if st.session_state.show_analytics:
        st.markdown("---")
        st.header("Analytics Dashboard")
        render_analytics_dashboard()

if __name__ == "__main__":
    main()
