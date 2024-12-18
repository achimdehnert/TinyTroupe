"""
Unit tests for the enhanced memory system.
"""

import unittest
import tempfile
import shutil
import os
import datetime
from pathlib import Path
import sqlite3
import json
import pickle

import numpy as np
from sentence_transformers import SentenceTransformer

from tinytroupe.enhanced_memory import MemoryChunk, EnhancedSemanticMemory

class TestEnhancedMemory(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test memories
        self.test_dir = tempfile.mkdtemp()
        self.memory = EnhancedSemanticMemory("test_agent", memory_dir=self.test_dir)

    def tearDown(self):
        """Clean up after each test."""
        if hasattr(self, 'memory'):
            # Clear all memories
            self.memory.clear()
            # Delete the database file
            try:
                os.remove(self.memory.db_path)
            except (OSError, PermissionError):
                pass  # Ignore errors if file is already deleted
            
        # Clean up temporary directory
        try:
            shutil.rmtree(self.test_dir)
        except (OSError, PermissionError):
            pass  # Ignore errors if directory is already deleted

    def test_memory_chunk_creation(self):
        """Test creation and serialization of memory chunks."""
        content = "Test memory content"
        source = "test"
        timestamp = datetime.datetime.now()
        metadata = {"type": "test"}
        embedding = np.random.rand(384)  # Default embedding size for 'all-MiniLM-L6-v2'

        chunk = MemoryChunk(content, source, timestamp, metadata, embedding)
        chunk_dict = chunk.to_dict()
        restored_chunk = MemoryChunk.from_dict(chunk_dict)

        self.assertEqual(chunk.content, restored_chunk.content)
        self.assertEqual(chunk.source, restored_chunk.source)
        self.assertEqual(chunk.metadata, restored_chunk.metadata)
        np.testing.assert_array_almost_equal(chunk.embedding, restored_chunk.embedding)

    def test_memory_storage_and_retrieval(self):
        """Test basic storage and retrieval of memories."""
        # Store some test memories
        self.memory.store("Memory about cats", "test", "episodic")
        self.memory.store("Memory about dogs", "test", "episodic")
        self.memory.store("Memory about birds", "test", "episodic")

        # Test retrieval
        results = self.memory.retrieve_relevant("cats", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertIn("cats", results[0]["content"])

    def test_memory_consolidation(self):
        """Test memory consolidation functionality."""
        # Store similar memories with a past timestamp
        past_time = datetime.datetime.now() - datetime.timedelta(days=2)
        
        with sqlite3.connect(self.memory.db_path) as conn:
            # Store memories directly with past timestamp
            embedding = self.memory.model.encode(["I saw a red car today"])[0]
            conn.execute(
                "INSERT INTO memories (content, source, timestamp, metadata, embedding, type, consolidated) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ("I saw a red car today", "test", past_time.isoformat(),
                 json.dumps({}), pickle.dumps(embedding), "episodic", 0)
            )
            
            embedding = self.memory.model.encode(["There was a red vehicle in the parking lot"])[0]
            conn.execute(
                "INSERT INTO memories (content, source, timestamp, metadata, embedding, type, consolidated) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ("There was a red vehicle in the parking lot", "test", past_time.isoformat(),
                 json.dumps({}), pickle.dumps(embedding), "episodic", 0)
            )
            
            embedding = self.memory.model.encode(["A crimson automobile was parked outside"])[0]
            conn.execute(
                "INSERT INTO memories (content, source, timestamp, metadata, embedding, type, consolidated) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ("A crimson automobile was parked outside", "test", past_time.isoformat(),
                 json.dumps({}), pickle.dumps(embedding), "episodic", 0)
            )
            conn.commit()

        # Force consolidation with a small time threshold
        self.memory.consolidate_memories(
            time_threshold=datetime.timedelta(seconds=1),
            similarity_threshold=0.7
        )

        # Check that semantic memories were created
        results = self.memory.retrieve_relevant("red car", top_k=5, memory_type="semantic")
        self.assertTrue(len(results) > 0, "No semantic memories were created after consolidation")
        
        # Verify that original memories were marked as consolidated
        with sqlite3.connect(self.memory.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM memories WHERE type = 'episodic' AND consolidated = 1")
            consolidated_count = cursor.fetchone()[0]
            self.assertTrue(consolidated_count > 0, "No episodic memories were marked as consolidated")

    def test_memory_persistence(self):
        """Test that memories persist between sessions."""
        # Store a memory
        self.memory.store("Persistent memory test", "test", "episodic")

        # Create a new memory instance with the same directory
        new_memory = EnhancedSemanticMemory("test_agent", memory_dir=self.test_dir)

        # Verify the memory is still there
        results = new_memory.retrieve_relevant("persistent", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertIn("Persistent", results[0]["content"])

    def test_memory_types(self):
        """Test handling of different memory types."""
        # Store different types of memories
        self.memory.store("Episodic memory", "test", "episodic")
        self.memory.store("Semantic memory", "test", "semantic")

        # Test retrieval by type
        episodic = self.memory.retrieve_relevant("memory", top_k=5, memory_type="episodic")
        semantic = self.memory.retrieve_relevant("memory", top_k=5, memory_type="semantic")

        self.assertTrue(any("Episodic" in m["content"] for m in episodic))
        self.assertTrue(any("Semantic" in m["content"] for m in semantic))

    def test_memory_clear(self):
        """Test memory clearing functionality."""
        # Store some memories
        self.memory.store("Test memory", "test", "episodic")
        
        # Clear memories
        self.memory.clear()
        
        # Verify no memories remain
        results = self.memory.retrieve_relevant("test", top_k=5)
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
