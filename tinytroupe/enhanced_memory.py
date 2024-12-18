"""
Enhanced memory system for TinyTroupe agents.
This module provides improved memory capabilities including better document indexing,
persistence, and memory consolidation mechanisms.
"""

import os
import json
import datetime
import logging
from typing import Any, List, Dict, Optional, Union
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
import pickle

from tinytroupe.utils import sanitize_raw_string

logger = logging.getLogger("tinytroupe")

class MemoryChunk:
    """A chunk of memory that can be stored and retrieved."""
    
    def __init__(self, content: str, source: str, timestamp: datetime.datetime,
                 metadata: Dict[str, Any] = None, embedding: np.ndarray = None):
        self.content = content
        self.source = source
        self.timestamp = timestamp
        self.metadata = metadata or {}
        self.embedding = embedding
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert the memory chunk to a dictionary for storage."""
        return {
            'content': self.content,
            'source': self.source,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata,
            'embedding': self.embedding.tolist() if self.embedding is not None else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryChunk':
        """Create a memory chunk from a dictionary."""
        return cls(
            content=data['content'],
            source=data['source'],
            timestamp=datetime.datetime.fromisoformat(data['timestamp']),
            metadata=data['metadata'],
            embedding=np.array(data['embedding']) if data['embedding'] is not None else None
        )

class EnhancedSemanticMemory:
    """
    Enhanced semantic memory with improved indexing, persistence, and consolidation.
    """
    
    def __init__(self, agent_name: str, memory_dir: str = None,
                 model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the enhanced semantic memory.
        
        Args:
            agent_name: Name of the agent this memory belongs to
            memory_dir: Directory to store persistent memory
            model_name: Name of the sentence transformer model to use
        """
        self.agent_name = agent_name
        self.memory_dir = memory_dir or os.path.join(os.getcwd(), 'agent_memories')
        self.db_path = os.path.join(self.memory_dir, f"{agent_name}_memory.db")
        
        # Create memory directory if it doesn't exist
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Initialize the embedding model
        self.model = SentenceTransformer(model_name)
        
        # Initialize the database
        self._init_database()
    
    def _get_connection(self):
        """Get a new database connection."""
        return sqlite3.connect(self.db_path)
    
    def _init_database(self):
        """Initialize the SQLite database for persistent storage."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    source TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata TEXT,
                    embedding BLOB,
                    type TEXT NOT NULL,
                    consolidated INTEGER DEFAULT 0
                )
            """)
            conn.commit()
    
    def store(self, content: str, source: str, memory_type: str = 'episodic',
              metadata: Dict[str, Any] = None) -> None:
        """
        Store a new memory.
        
        Args:
            content: The content to store
            source: Source of the memory (e.g., 'conversation', 'document', etc.)
            memory_type: Type of memory ('episodic' or 'semantic')
            metadata: Additional metadata about the memory
        """
        # Create embedding
        embedding = self.model.encode([content])[0]
        
        # Create memory chunk
        chunk = MemoryChunk(
            content=content,
            source=source,
            timestamp=datetime.datetime.now(),
            metadata=metadata,
            embedding=embedding
        )
        
        # Store in database
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO memories (content, source, timestamp, metadata, embedding, type) VALUES (?, ?, ?, ?, ?, ?)",
                (chunk.content, chunk.source, chunk.timestamp.isoformat(),
                 json.dumps(chunk.metadata), pickle.dumps(chunk.embedding), memory_type)
            )
            conn.commit()
    
    def retrieve_relevant(self, query: str, top_k: int = 5,
                         memory_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve memories relevant to a query.
        
        Args:
            query: The query to search for
            top_k: Number of results to return
            memory_type: Optional filter for memory type
        
        Returns:
            List of relevant memories with their similarity scores
        """
        # Get query embedding
        query_embedding = self.model.encode([query])[0]
        
        # Retrieve all memories
        with self._get_connection() as conn:
            if memory_type:
                cursor = conn.execute(
                    "SELECT content, source, timestamp, metadata, embedding FROM memories WHERE type = ?",
                    (memory_type,)
                )
            else:
                cursor = conn.execute(
                    "SELECT content, source, timestamp, metadata, embedding FROM memories"
                )
            
            memories = []
            for row in cursor:
                content, source, timestamp, metadata_str, embedding_bytes = row
                embedding = pickle.loads(embedding_bytes)
                metadata = json.loads(metadata_str)
                
                # Calculate similarity
                similarity = cosine_similarity([query_embedding], [embedding])[0][0]
                
                memories.append({
                    'content': content,
                    'source': source,
                    'timestamp': timestamp,
                    'metadata': metadata,
                    'similarity': float(similarity)
                })
        
        # Sort by similarity and return top_k
        memories.sort(key=lambda x: x['similarity'], reverse=True)
        return memories[:top_k]
    
    def consolidate_memories(self, time_threshold: datetime.timedelta = datetime.timedelta(days=1),
                           similarity_threshold: float = 0.8) -> None:
        """
        Consolidate episodic memories into semantic memories.
        
        Args:
            time_threshold: Time threshold for considering memories for consolidation
            similarity_threshold: Similarity threshold for grouping related memories
        """
        cutoff_time = datetime.datetime.now() - time_threshold
        
        with self._get_connection() as conn:
            try:
                # Get unconsolidated episodic memories older than the threshold
                cursor = conn.execute(
                    """
                    SELECT id, content, embedding FROM memories 
                    WHERE type = 'episodic' AND consolidated = 0 
                    AND datetime(timestamp) < datetime(?)
                    """,
                    (cutoff_time.isoformat(),)
                )
                
                memories = [(id_, content, pickle.loads(embedding)) 
                           for id_, content, embedding in cursor]
                
                if not memories:
                    logger.debug("No memories found for consolidation")
                    return
                
                # Group similar memories
                consolidated_groups = []
                used_indices = set()
                
                for i, (id1, content1, emb1) in enumerate(memories):
                    if i in used_indices:
                        continue
                        
                    group = [(id1, content1)]
                    used_indices.add(i)
                    
                    for j, (id2, content2, emb2) in enumerate(memories[i+1:], i+1):
                        if j in used_indices:
                            continue
                            
                        similarity = cosine_similarity([emb1], [emb2])[0][0]
                        if similarity >= similarity_threshold:
                            group.append((id2, content2))
                            used_indices.add(j)
                    
                    if len(group) > 1:  # Only consolidate if there are multiple similar memories
                        consolidated_groups.append(group)
                
                # Create consolidated memories and update database
                for group in consolidated_groups:
                    # Combine contents and create a new semantic memory
                    combined_content = "\n".join(content for _, content in group)
                    self.store(
                        content=combined_content,
                        source="memory_consolidation",
                        memory_type="semantic",
                        metadata={"consolidated_from": [id_ for id_, _ in group]}
                    )
                    
                    # Mark original memories as consolidated
                    for id_, _ in group:
                        conn.execute(
                            "UPDATE memories SET consolidated = 1 WHERE id = ?",
                            (id_,)
                        )
                
                conn.commit()
                
            except sqlite3.Error as e:
                logger.error(f"Database error during consolidation: {e}")
                conn.rollback()
                raise
    
    def clear(self) -> None:
        """Clear all memories."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM memories")
            conn.commit()
