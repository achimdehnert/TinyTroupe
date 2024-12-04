"""
Module for generating synthetic data for discussions and simulations.
"""
from typing import Dict, List, Any, Optional
import json
import random
from datetime import datetime, timedelta
from ..core.base_discussion import DiscussionType

class SyntheticDataGenerator:
    """Generator for synthetic discussion data."""
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize data generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        if seed is not None:
            random.seed(seed)
            
    def generate_discussion_data(
        self,
        discussion_type: DiscussionType,
        num_participants: int = 4,
        num_steps: int = 3
    ) -> Dict[str, Any]:
        """
        Generate synthetic discussion data.
        
        Args:
            discussion_type: Type of discussion
            num_participants: Number of participants
            num_steps: Number of discussion steps
            
        Returns:
            Generated discussion data
        """
        participants = self._generate_participants(num_participants)
        steps = []
        
        for step in range(num_steps):
            step_data = self._generate_step_data(
                step,
                participants,
                discussion_type
            )
            steps.append(step_data)
            
        return {
            "metadata": self._generate_metadata(discussion_type),
            "participants": participants,
            "steps": steps,
            "summary": self._generate_summary(steps, discussion_type)
        }
        
    def _generate_participants(self, num_participants: int) -> List[Dict[str, Any]]:
        """Generate participant data."""
        roles = [
            "Moderator",
            "Expert",
            "Critic",
            "Observer",
            "Innovator",
            "Analyst",
            "User Advocate",
            "Technical Lead"
        ]
        
        personalities = [
            "analytical",
            "creative",
            "diplomatic",
            "assertive",
            "collaborative",
            "detail-oriented",
            "big-picture",
            "pragmatic"
        ]
        
        participants = []
        for i in range(num_participants):
            participant = {
                "id": f"P{i+1}",
                "role": roles[i % len(roles)],
                "personality": personalities[i % len(personalities)],
                "expertise_level": random.uniform(0.6, 1.0),
                "engagement_score": random.uniform(0.7, 1.0)
            }
            participants.append(participant)
            
        return participants
        
    def _generate_step_data(
        self,
        step: int,
        participants: List[Dict[str, Any]],
        discussion_type: DiscussionType
    ) -> Dict[str, Any]:
        """Generate data for a discussion step."""
        responses = []
        
        for participant in participants:
            response = self._generate_response(
                participant,
                step,
                discussion_type
            )
            responses.append(response)
            
        return {
            "step_number": step + 1,
            "timestamp": (
                datetime.now() + timedelta(minutes=15*step)
            ).isoformat(),
            "phase": self._get_phase_name(step, discussion_type),
            "responses": responses,
            "interactions": self._generate_interactions(participants),
            "metrics": self._generate_step_metrics()
        }
        
    def _generate_response(
        self,
        participant: Dict[str, Any],
        step: int,
        discussion_type: DiscussionType
    ) -> Dict[str, Any]:
        """Generate a participant response."""
        base_response = {
            "participant_id": participant["id"],
            "content_length": random.randint(50, 200),
            "sentiment_score": random.uniform(0.3, 0.9),
            "relevance_score": random.uniform(
                0.5 + participant["expertise_level"]*0.2,
                0.9 + participant["expertise_level"]*0.1
            )
        }
        
        # Add type-specific content
        if discussion_type == DiscussionType.BRAINSTORMING:
            base_response.update({
                "num_ideas": random.randint(1, 4),
                "creativity_score": random.uniform(0.4, 0.9),
                "feasibility_score": random.uniform(0.3, 0.8)
            })
        elif discussion_type == DiscussionType.EVALUATION:
            base_response.update({
                "rating": random.uniform(1, 5),
                "confidence_score": random.uniform(0.6, 0.9),
                "criteria_coverage": random.uniform(0.7, 1.0)
            })
        elif discussion_type == DiscussionType.INTERVIEW:
            base_response.update({
                "answer_completeness": random.uniform(0.5, 1.0),
                "detail_level": random.uniform(0.6, 0.9),
                "follow_up_questions": random.randint(0, 3)
            })
            
        return base_response
        
    def _generate_interactions(
        self,
        participants: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate interaction data between participants."""
        num_interactions = random.randint(
            len(participants),
            len(participants) * 2
        )
        
        interactions = []
        for _ in range(num_interactions):
            p1, p2 = random.sample(participants, 2)
            interaction = {
                "from_id": p1["id"],
                "to_id": p2["id"],
                "type": random.choice([
                    "question",
                    "agreement",
                    "disagreement",
                    "buildup",
                    "clarification"
                ]),
                "strength": random.uniform(0.1, 1.0)
            }
            interactions.append(interaction)
            
        return interactions
        
    def _generate_step_metrics(self) -> Dict[str, float]:
        """Generate metrics for a discussion step."""
        return {
            "participation_balance": random.uniform(0.6, 1.0),
            "discussion_depth": random.uniform(0.4, 0.9),
            "convergence_rate": random.uniform(0.3, 0.8),
            "idea_flow_rate": random.uniform(0.5, 1.0)
        }
        
    def _generate_metadata(self, discussion_type: DiscussionType) -> Dict[str, Any]:
        """Generate discussion metadata."""
        return {
            "type": discussion_type.value,
            "generated_at": datetime.now().isoformat(),
            "version": "1.0",
            "seed": self.seed
        }
        
    def _generate_summary(
        self,
        steps: List[Dict[str, Any]],
        discussion_type: DiscussionType
    ) -> Dict[str, Any]:
        """Generate discussion summary."""
        return {
            "total_steps": len(steps),
            "average_metrics": self._average_step_metrics(steps),
            "participation_stats": self._calculate_participation_stats(steps),
            "outcome_metrics": self._generate_outcome_metrics(discussion_type)
        }
        
    def _average_step_metrics(
        self,
        steps: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate average metrics across steps."""
        all_metrics = {}
        for step in steps:
            for key, value in step["metrics"].items():
                if key not in all_metrics:
                    all_metrics[key] = []
                all_metrics[key].append(value)
                
        return {
            key: sum(values) / len(values)
            for key, values in all_metrics.items()
        }
        
    def _calculate_participation_stats(
        self,
        steps: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate participation statistics."""
        participant_responses = {}
        
        for step in steps:
            for response in step["responses"]:
                pid = response["participant_id"]
                if pid not in participant_responses:
                    participant_responses[pid] = []
                participant_responses[pid].append(response)
                
        return {
            "response_distribution": {
                pid: len(responses)
                for pid, responses in participant_responses.items()
            },
            "engagement_levels": {
                pid: sum(r["relevance_score"] for r in responses) / len(responses)
                for pid, responses in participant_responses.items()
            }
        }
        
    def _generate_outcome_metrics(
        self,
        discussion_type: DiscussionType
    ) -> Dict[str, float]:
        """Generate outcome-specific metrics."""
        base_metrics = {
            "objective_achievement": random.uniform(0.6, 0.95),
            "consensus_level": random.uniform(0.5, 0.9),
            "action_clarity": random.uniform(0.7, 1.0)
        }
        
        if discussion_type == DiscussionType.BRAINSTORMING:
            base_metrics.update({
                "idea_quality": random.uniform(0.6, 0.9),
                "innovation_level": random.uniform(0.5, 0.95),
                "implementation_feasibility": random.uniform(0.4, 0.8)
            })
        elif discussion_type == DiscussionType.EVALUATION:
            base_metrics.update({
                "decision_confidence": random.uniform(0.7, 0.95),
                "criteria_coverage": random.uniform(0.8, 1.0),
                "evaluation_thoroughness": random.uniform(0.75, 0.95)
            })
        elif discussion_type == DiscussionType.INTERVIEW:
            base_metrics.update({
                "information_completeness": random.uniform(0.7, 0.9),
                "insight_depth": random.uniform(0.6, 0.85),
                "follow_up_potential": random.uniform(0.5, 0.8)
            })
            
        return base_metrics
        
    def _get_phase_name(self, step: int, discussion_type: DiscussionType) -> str:
        """Get phase name based on step and discussion type."""
        phase_maps = {
            DiscussionType.BRAINSTORMING: [
                "ideation",
                "elaboration",
                "evaluation",
                "refinement"
            ],
            DiscussionType.EVALUATION: [
                "criteria_review",
                "assessment",
                "discussion",
                "conclusion"
            ],
            DiscussionType.INTERVIEW: [
                "introduction",
                "core_questions",
                "deep_dive",
                "wrap_up"
            ]
        }
        
        phases = phase_maps.get(
            discussion_type,
            ["start", "middle", "end", "conclusion"]
        )
        return phases[min(step, len(phases)-1)]
