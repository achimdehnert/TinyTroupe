"""
Enhanced memory system that combines episodic and semantic memories.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class Memory:
    def __init__(self, content: str, context: Dict[str, Any], timestamp: Optional[datetime] = None):
        self.content = content
        self.context = context
        self.timestamp = timestamp or datetime.now()
        self.embedding = None

class EnhancedMemorySystem:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.episodic_memories: List[Memory] = []
        self.semantic_memories: List[Memory] = []
        
    def store_episodic_memory(self, content: str, context: Dict[str, Any]) -> Memory:
        """Store a new episodic memory."""
        memory = Memory(content, context)
        memory.embedding = self.model.encode([content])[0]
        self.episodic_memories.append(memory)
        return memory
    
    def search_memories(self, query: str, k: int = 5) -> List[Memory]:
        """Search for relevant memories using semantic similarity."""
        query_embedding = self.model.encode([query])[0]
        
        all_memories = self.episodic_memories + self.semantic_memories
        if not all_memories:
            return []
        
        # Calculate similarities
        memory_embeddings = np.array([m.embedding for m in all_memories])
        similarities = cosine_similarity([query_embedding], memory_embeddings)[0]
        
        # Get top k results
        top_indices = np.argsort(similarities)[-k:][::-1]
        return [all_memories[i] for i in top_indices]
    
    def consolidate_memories(self, threshold: float = 0.8) -> List[Memory]:
        """Consolidate similar episodic memories into semantic memories."""
        if len(self.episodic_memories) < 2:
            return []
        
        # Calculate similarity matrix
        embeddings = np.array([m.embedding for m in self.episodic_memories])
        similarity_matrix = cosine_similarity(embeddings)
        
        # Find groups of similar memories
        consolidated = []
        processed = set()
        
        for i in range(len(self.episodic_memories)):
            if i in processed:
                continue
                
            # Find similar memories
            similar_indices = np.where(similarity_matrix[i] > threshold)[0]
            if len(similar_indices) > 1:  # Only consolidate if we have multiple similar memories
                similar_memories = [self.episodic_memories[j] for j in similar_indices]
                
                # Create consolidated memory
                combined_content = "\n".join([m.content for m in similar_memories])
                combined_context = {
                    "source_memories": len(similar_memories),
                    "time_range": {
                        "start": min(m.timestamp for m in similar_memories),
                        "end": max(m.timestamp for m in similar_memories)
                    }
                }
                
                semantic_memory = Memory(combined_content, combined_context)
                semantic_memory.embedding = self.model.encode([combined_content])[0]
                
                consolidated.append(semantic_memory)
                processed.update(similar_indices)
        
        # Add consolidated memories to semantic memories
        self.semantic_memories.extend(consolidated)
        
        # Remove consolidated episodic memories
        self.episodic_memories = [
            m for i, m in enumerate(self.episodic_memories)
            if i not in processed
        ]
        
        return consolidated
