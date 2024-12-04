"""
Unit tests for the result processor module.
"""
import unittest
from group_cases.src.utils.result_processor import (
    format_results,
    format_brainstorming_results,
    format_evaluation_results,
    format_interview_results,
    format_generic_results
)

class TestResultProcessor(unittest.TestCase):
    """Test cases for result processing functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_results = [
            {
                "phase": "phase1",
                "responses": [
                    {
                        "agent": "Agent1",
                        "response": "Response1",
                        "ideas": ["idea1", "idea2"],
                        "theme": "theme1",
                        "content": "content1",
                        "priority": 1
                    }
                ],
                "summary": {
                    "key_points": ["point1"],
                    "consensus": "consensus1",
                    "action_items": ["action1"]
                }
            }
        ]
        
    def test_format_brainstorming_results(self):
        """Test brainstorming results formatting."""
        results = format_brainstorming_results(self.sample_results)
        
        self.assertIn("ideas", results)
        self.assertIn("themes", results)
        self.assertIn("priorities", results)
        self.assertIn("summary", results)
        
        self.assertEqual(len(results["ideas"]), 2)
        self.assertIn("theme1", results["themes"])
        self.assertEqual(results["priorities"]["content1"], 1)
        
    def test_format_evaluation_results(self):
        """Test evaluation results formatting."""
        # Add evaluation-specific data
        self.sample_results[0]["responses"][0]["scores"] = {
            "criterion1": 4.5
        }
        self.sample_results[0]["responses"][0]["insights"] = ["insight1"]
        self.sample_results[0]["responses"][0]["recommendations"] = ["rec1"]
        
        results = format_evaluation_results(self.sample_results)
        
        self.assertIn("scores", results)
        self.assertIn("insights", results)
        self.assertIn("recommendations", results)
        self.assertIn("summary", results)
        
        self.assertIn("criterion1", results["scores"])
        self.assertEqual(len(results["insights"]), 1)
        self.assertEqual(len(results["recommendations"]), 1)
        
    def test_format_interview_results(self):
        """Test interview results formatting."""
        # Add interview-specific data
        self.sample_results[0]["responses"][0]["findings"] = ["finding1"]
        self.sample_results[0]["responses"][0]["quotes"] = ["quote1"]
        
        results = format_interview_results(self.sample_results)
        
        self.assertIn("key_findings", results)
        self.assertIn("quotes", results)
        self.assertIn("themes", results)
        self.assertIn("summary", results)
        
        self.assertEqual(len(results["key_findings"]), 1)
        self.assertEqual(len(results["quotes"]), 1)
        self.assertIn("theme1", results["themes"])
        
    def test_format_generic_results(self):
        """Test generic results formatting."""
        results = format_generic_results(self.sample_results)
        
        self.assertIn("key_points", results)
        self.assertIn("consensus", results)
        self.assertIn("action_items", results)
        self.assertIn("summary", results)
        
        self.assertEqual(len(results["key_points"]), 1)
        self.assertEqual(len(results["consensus"]), 1)
        self.assertEqual(len(results["action_items"]), 1)
        
    def test_format_results_dispatcher(self):
        """Test result format dispatching."""
        # Test each discussion type
        for discussion_type in ["brainstorming", "evaluation", "interview"]:
            results = format_results(self.sample_results, discussion_type)
            self.assertIsInstance(results, dict)
            self.assertIn("summary", results)
            
        # Test unknown type falls back to generic
        results = format_results(self.sample_results, "unknown_type")
        self.assertIn("key_points", results)
        self.assertIn("consensus", results)
        
if __name__ == '__main__':
    unittest.main()
