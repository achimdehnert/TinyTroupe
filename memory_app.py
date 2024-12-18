"""
Streamlit app for interacting with the enhanced memory system.
"""

import os
import datetime
import streamlit as st
from tinytroupe.enhanced_memory import EnhancedSemanticMemory

# Initialize session state
if 'memory' not in st.session_state:
    # Create a directory for memories in the user's home directory
    memory_dir = os.path.join(os.path.expanduser("~"), ".tinytroupe_memories")
    os.makedirs(memory_dir, exist_ok=True)
    st.session_state.memory = EnhancedSemanticMemory("streamlit_agent", memory_dir=memory_dir)

def store_memory():
    """Store a new memory."""
    memory_content = st.session_state.memory_content
    memory_source = st.session_state.memory_source
    memory_type = st.session_state.memory_type
    
    if memory_content and memory_source:
        try:
            st.session_state.memory.store(
                content=memory_content,
                source=memory_source,
                memory_type=memory_type
            )
            st.success("Memory stored successfully!")
            # Clear the input fields
            st.session_state.memory_content = ""
            st.session_state.memory_source = ""
        except Exception as e:
            st.error(f"Error storing memory: {str(e)}")

def search_memories():
    """Search for relevant memories."""
    query = st.session_state.search_query
    memory_type = st.session_state.search_type
    top_k = st.session_state.top_k
    
    if query:
        try:
            results = st.session_state.memory.retrieve_relevant(
                query=query,
                top_k=top_k,
                memory_type=memory_type if memory_type != "all" else None
            )
            
            if results:
                for i, result in enumerate(results, 1):
                    with st.expander(f"Memory {i} (Similarity: {result['similarity']:.2f})"):
                        st.write("Content:", result["content"])
                        st.write("Source:", result["source"])
                        st.write("Timestamp:", result["timestamp"])
                        st.write("Metadata:", result["metadata"])
            else:
                st.info("No relevant memories found.")
        except Exception as e:
            st.error(f"Error searching memories: {str(e)}")

def consolidate_memories():
    """Consolidate episodic memories into semantic memories."""
    try:
        days = st.session_state.consolidation_days
        similarity = st.session_state.similarity_threshold
        
        st.session_state.memory.consolidate_memories(
            time_threshold=datetime.timedelta(days=days),
            similarity_threshold=similarity
        )
        st.success("Memories consolidated successfully!")
    except Exception as e:
        st.error(f"Error consolidating memories: {str(e)}")

# Set up the Streamlit interface
st.title("Enhanced Memory System")
st.markdown("""
This app demonstrates the enhanced memory capabilities of TinyTroupe agents.
You can store new memories, search through existing ones, and consolidate related memories.
""")

# Create tabs for different functions
tab1, tab2, tab3 = st.tabs(["Store Memory", "Search Memories", "Consolidate"])

# Tab 1: Store Memory
with tab1:
    st.header("Store New Memory")
    
    if "memory_content" not in st.session_state:
        st.session_state.memory_content = ""
    if "memory_source" not in st.session_state:
        st.session_state.memory_source = ""
    if "memory_type" not in st.session_state:
        st.session_state.memory_type = "episodic"
    
    st.text_area("Memory Content", key="memory_content", height=150)
    st.text_input("Source", key="memory_source", placeholder="e.g., conversation, document, observation")
    st.selectbox("Memory Type", ["episodic", "semantic"], key="memory_type")
    st.button("Store Memory", on_click=store_memory)

# Tab 2: Search Memories
with tab2:
    st.header("Search Memories")
    
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "search_type" not in st.session_state:
        st.session_state.search_type = "all"
    if "top_k" not in st.session_state:
        st.session_state.top_k = 5
    
    st.text_input("Search Query", key="search_query")
    st.selectbox("Memory Type", ["all", "episodic", "semantic"], key="search_type")
    st.slider("Number of Results", 1, 20, key="top_k")
    st.button("Search", on_click=search_memories)

# Tab 3: Consolidate Memories
with tab3:
    st.header("Consolidate Memories")
    st.markdown("""
    Consolidate episodic memories into semantic memories based on time and similarity thresholds.
    This process helps in creating higher-level understanding from individual experiences.
    """)
    
    if "consolidation_days" not in st.session_state:
        st.session_state.consolidation_days = 1
    if "similarity_threshold" not in st.session_state:
        st.session_state.similarity_threshold = 0.8
    
    st.slider("Days Threshold", 0.0, 30.0, key="consolidation_days")
    st.slider("Similarity Threshold", 0.0, 1.0, key="similarity_threshold")
    st.button("Consolidate", on_click=consolidate_memories)
