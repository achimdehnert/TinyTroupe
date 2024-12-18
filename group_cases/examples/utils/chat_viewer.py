import streamlit as st
import subprocess
import re

def run_chat():
    result = subprocess.run(['python', 'simple_chat.py'], 
                          capture_output=True, 
                          text=True)
    return result.stdout

def parse_chat(chat_output):
    messages = []
    current_message = {}
    
    for line in chat_output.split('\n'):
        line = line.strip()
        if not line or line.startswith('!!!!') or line.startswith('Looking for') or line.startswith('====='):
            continue
            
        if '-->' in line:
            if current_message:
                messages.append(current_message)
                current_message = {}
            
            parts = line.split('-->')
            sender = parts[0].strip()
            receiver = parts[1].split(':')[0].strip()
            msg_type = parts[1].split(':')[1].strip() if ':' in parts[1] else ''
            
            current_message = {
                'sender': sender,
                'receiver': receiver,
                'type': msg_type,
                'content': []
            }
        elif line and current_message:
            if not line.startswith('>>>>>>>'):
                current_message['content'].append(line)
    
    if current_message:
        messages.append(current_message)
    
    return messages

def display_chat(messages):
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .chat-container {
            margin: 0.5rem 0;
            padding: 0.5rem;
        }
        .sender {
            font-size: 0.8rem;
            margin-bottom: 0.2rem;
            color: #666;
        }
        .message {
            padding: 0.5rem 1rem;
            border-radius: 15px;
            max-width: 80%;
            margin: 0.2rem 0;
        }
        .user-message {
            background-color: #1982FC;
            color: white;
            float: right;
        }
        .ai-message {
            background-color: #f0f2f6;
            color: black;
            float: left;
        }
        .social-message {
            text-align: center;
            color: #666;
            font-style: italic;
            font-size: 0.8rem;
            margin: 0.5rem 0;
        }
        .clear {
            clear: both;
        }
        </style>
    """, unsafe_allow_html=True)
    
    for msg in messages:
        if msg['type'] in ['[THOUGHT]', '[REACH_OUT]', '[DONE]']:
            continue
            
        if msg['type'] == '[CONVERSATION]':
            is_user = msg['sender'] == 'USER'
            
            message_html = f"""
            <div class="chat-container">
                <div class="sender">{'You' if is_user else msg['sender']}</div>
                <div class="message {'user-message' if is_user else 'ai-message'}">
                    {''.join(msg['content'])}
                </div>
                <div class="clear"></div>
            </div>
            """
            st.markdown(message_html, unsafe_allow_html=True)
        
        elif msg['type'] == '[SOCIAL]':
            st.markdown(f'<div class="social-message">{"".join(msg["content"])}</div>', 
                       unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="TinyTroupe Chat", layout="wide")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown("# 🎮 Controls")
        if st.button("🔄 Start New Chat", use_container_width=True):
            with st.spinner("🤖 Starting conversation..."):
                chat_output = run_chat()
                messages = parse_chat(chat_output)
                st.session_state.chat_history = messages
    
    # Main chat area with three columns
    left_col, main_col, right_col = st.columns([1, 2, 1])
    
    with main_col:
        st.markdown("# 💬 TinyTroupe Chat")
        st.markdown("---")
        
        if st.session_state.chat_history:
            display_chat(st.session_state.chat_history)
        else:
            st.markdown("""
                <div style='text-align: center; padding: 2rem; background-color: #f0f2f6; border-radius: 10px;'>
                    <h3>👋 Welcome!</h3>
                    <p>Click '🔄 Start New Chat' in the sidebar to begin a conversation</p>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
