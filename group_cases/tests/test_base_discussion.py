"""
Unit tests for the base discussion module.
"""
import unittest
import json
import os
from tempfile import TemporaryDirectory
from group_cases.src.core.base_discussion import BaseDiscussion, DiscussionType

class MockDiscussion(BaseDiscussion):
    """Mock discussion class for testing."""
    def run_discussion(self, num_steps=3):
        return {"mock_results": True}

class TestBaseDiscussion(unittest.TestCase):
    """Test cases for BaseDiscussion class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.discussion = MockDiscussion(
            name="Test Discussion",
            discussion_type=DiscussionType.BRAINSTORMING
        )
        
    def test_initialization(self):
        """Test discussion initialization."""
        self.assertEqual(self.discussion.name, "Test Discussion")
        self.assertEqual(
            self.discussion.discussion_type,
            DiscussionType.BRAINSTORMING
        )
        self.assertEqual(
            self.discussion.metadata["name"],
            "Test Discussion"
        )
        
    def test_add_context(self):
        """Test adding context information."""
        self.discussion.add_context("test_key", "test_value")
        self.assertEqual(
            self.discussion.context["test_key"],
            "test_value"
        )
        
    def test_add_metadata(self):
        """Test adding metadata information."""
        self.discussion.add_metadata("test_key", "test_value")
        self.assertEqual(
            self.discussion.metadata["test_key"],
            "test_value"
        )
        
    def test_prepare_extraction_config(self):
        """Test extraction configuration preparation."""
        self.discussion.add_context("ctx_key", "ctx_value")
        self.discussion.add_metadata("meta_key", "meta_value")
        
        config = self.discussion.prepare_extraction_config()
        
        self.assertEqual(config["context"]["ctx_key"], "ctx_value")
        self.assertEqual(config["metadata"]["meta_key"], "meta_value")
        
    def test_save_results(self):
        """Test saving discussion results."""
        with TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_results.json")
            results = {"test": "results"}
            
            self.discussion.save_results(results, filepath)
            
            # Verify file was created and contains correct data
            self.assertTrue(os.path.exists(filepath))
            
            with open(filepath, 'r') as f:
                saved_data = json.load(f)
                
            self.assertEqual(saved_data["results"], results)
            self.assertEqual(
                saved_data["metadata"]["name"],
                "Test Discussion"
            )
            
if __name__ == '__main__':
    unittest.main()
