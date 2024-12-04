"""
Unit tests for synthetic data generation.
"""
import unittest
from datetime import datetime
from group_cases.src.utils.synthetic_data import SyntheticDataGenerator
from group_cases.src.core.base_discussion import DiscussionType

class TestSyntheticDataGenerator(unittest.TestCase):
    """Test cases for SyntheticDataGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = SyntheticDataGenerator(seed=42)
        
    def test_generate_discussion_data(self):
        """Test complete discussion data generation."""
        data = self.generator.generate_discussion_data(
            DiscussionType.BRAINSTORMING,
            num_participants=3,
            num_steps=2
        )
        
        # Check basic structure
        self.assertIn("metadata", data)
        self.assertIn("participants", data)
        self.assertIn("steps", data)
        self.assertIn("summary", data)
        
        # Check participants
        self.assertEqual(len(data["participants"]), 3)
        for participant in data["participants"]:
            self.assertIn("id", participant)
            self.assertIn("role", participant)
            self.assertIn("personality", participant)
            
        # Check steps
        self.assertEqual(len(data["steps"]), 2)
        for step in data["steps"]:
            self.assertIn("step_number", step)
            self.assertIn("timestamp", step)
            self.assertIn("phase", step)
            self.assertIn("responses", step)
            self.assertEqual(len(step["responses"]), 3)
            
    def test_different_discussion_types(self):
        """Test data generation for different discussion types."""
        for discussion_type in DiscussionType:
            data = self.generator.generate_discussion_data(discussion_type)
            
            # Check type-specific content
            for step in data["steps"]:
                for response in step["responses"]:
                    if discussion_type == DiscussionType.BRAINSTORMING:
                        self.assertIn("num_ideas", response)
                        self.assertIn("creativity_score", response)
                    elif discussion_type == DiscussionType.EVALUATION:
                        self.assertIn("rating", response)
                        self.assertIn("confidence_score", response)
                    elif discussion_type == DiscussionType.INTERVIEW:
                        self.assertIn("answer_completeness", response)
                        self.assertIn("follow_up_questions", response)
                        
    def test_reproducibility(self):
        """Test that same seed produces same results."""
        gen1 = SyntheticDataGenerator(seed=42)
        gen2 = SyntheticDataGenerator(seed=42)
        
        data1 = gen1.generate_discussion_data(DiscussionType.BRAINSTORMING)
        data2 = gen2.generate_discussion_data(DiscussionType.BRAINSTORMING)
        
        # Compare key metrics
        self.assertEqual(
            data1["summary"]["average_metrics"],
            data2["summary"]["average_metrics"]
        )
        
    def test_participant_generation(self):
        """Test participant data generation."""
        participants = self.generator._generate_participants(4)
        
        self.assertEqual(len(participants), 4)
        for participant in participants:
            self.assertIn("id", participant)
            self.assertIn("role", participant)
            self.assertIn("personality", participant)
            self.assertIn("expertise_level", participant)
            self.assertIn("engagement_score", participant)
            
            # Check value ranges
            self.assertGreaterEqual(participant["expertise_level"], 0.6)
            self.assertLessEqual(participant["expertise_level"], 1.0)
            self.assertGreaterEqual(participant["engagement_score"], 0.7)
            self.assertLessEqual(participant["engagement_score"], 1.0)
            
    def test_step_metrics(self):
        """Test step metrics generation."""
        metrics = self.generator._generate_step_metrics()
        
        expected_metrics = [
            "participation_balance",
            "discussion_depth",
            "convergence_rate",
            "idea_flow_rate"
        ]
        
        for metric in expected_metrics:
            self.assertIn(metric, metrics)
            self.assertGreaterEqual(metrics[metric], 0.0)
            self.assertLessEqual(metrics[metric], 1.0)
            
    def test_metadata(self):
        """Test metadata generation."""
        metadata = self.generator._generate_metadata(DiscussionType.BRAINSTORMING)
        
        self.assertEqual(metadata["type"], DiscussionType.BRAINSTORMING.value)
        self.assertEqual(metadata["version"], "1.0")
        self.assertEqual(metadata["seed"], 42)
        
        # Check timestamp format
        try:
            datetime.fromisoformat(metadata["generated_at"])
        except ValueError:
            self.fail("Invalid timestamp format")
            
    def test_phase_names(self):
        """Test phase name generation."""
        # Test brainstorming phases
        phase = self.generator._get_phase_name(
            0,
            DiscussionType.BRAINSTORMING
        )
        self.assertEqual(phase, "ideation")
        
        # Test evaluation phases
        phase = self.generator._get_phase_name(
            1,
            DiscussionType.EVALUATION
        )
        self.assertEqual(phase, "assessment")
        
        # Test interview phases
        phase = self.generator._get_phase_name(
            2,
            DiscussionType.INTERVIEW
        )
        self.assertEqual(phase, "deep_dive")
        
if __name__ == '__main__':
    unittest.main()
