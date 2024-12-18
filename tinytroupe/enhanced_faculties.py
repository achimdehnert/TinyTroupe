"""
Enhanced mental faculties for TinyTroupe agents.
Provides improved cognitive abilities including emotional intelligence,
advanced reasoning, and specialized skills.
"""

from typing import Any, Dict, List, Optional
import datetime
import logging
import json

from tinytroupe.agent import TinyMentalFaculty

logger = logging.getLogger("tinytroupe")

class EmotionalIntelligenceFaculty(TinyMentalFaculty):
    """
    Provides emotional intelligence capabilities to an agent.
    Includes emotion recognition, empathy, and emotional regulation.
    """
    
    def __init__(self):
        super().__init__("Emotional Intelligence")
        self.current_emotional_state = {
            "valence": 0.0,  # -1 (negative) to 1 (positive)
            "arousal": 0.0,  # 0 (calm) to 1 (excited)
            "dominance": 0.5,  # 0 (submissive) to 1 (dominant)
            "emotions": [],   # List of active emotions
            "intensity": 0.5  # Overall emotional intensity
        }
        self.emotion_history = []
        
    def process_action(self, agent, action: dict) -> bool:
        """Process emotional intelligence related actions."""
        if action["type"] == "ANALYZE_EMOTION":
            return self._analyze_emotion(agent, action["content"])
        elif action["type"] == "REGULATE_EMOTION":
            return self._regulate_emotion(agent, action["content"])
        elif action["type"] == "SHOW_EMPATHY":
            return self._show_empathy(agent, action["content"])
        elif action["type"] == "UPDATE_EMOTIONAL_STATE":
            return self._update_emotional_state(agent, action["content"])
        return False

    def _analyze_emotion(self, agent, content: str) -> bool:
        """Analyze emotional content of text using predefined emotional markers."""
        emotion_markers = {
            "joy": ["happy", "excited", "delighted", "pleased"],
            "sadness": ["sad", "disappointed", "unhappy", "down"],
            "anger": ["angry", "frustrated", "annoyed", "irritated"],
            "fear": ["afraid", "worried", "anxious", "concerned"],
            "surprise": ["surprised", "amazed", "astonished", "shocked"],
            "trust": ["trust", "confident", "reliable", "dependable"]
        }
        
        detected_emotions = []
        content_lower = content.lower()
        
        for emotion, markers in emotion_markers.items():
            if any(marker in content_lower for marker in markers):
                detected_emotions.append(emotion)
        
        if detected_emotions:
            self._update_emotional_state(agent, {
                "emotions": detected_emotions,
                "intensity": len(detected_emotions) / len(emotion_markers)
            })
            return True
        return False

    def _regulate_emotion(self, agent, strategy: dict) -> bool:
        """Apply emotional regulation strategies."""
        valid_strategies = {
            "reappraisal": self._apply_reappraisal,
            "suppression": self._apply_suppression,
            "acceptance": self._apply_acceptance
        }
        
        if strategy["type"] in valid_strategies:
            return valid_strategies[strategy["type"]](agent, strategy)
        return False

    def _update_emotional_state(self, agent, new_state: dict) -> bool:
        """Update the agent's emotional state and record in history."""
        timestamp = datetime.datetime.now().isoformat()
        
        # Update current state
        self.current_emotional_state.update(new_state)
        
        # Record in history
        self.emotion_history.append({
            "timestamp": timestamp,
            "state": self.current_emotional_state.copy(),
            "context": agent._configuration.get("current_context", "")
        })
        
        # Store in agent's episodic memory
        if hasattr(agent, "episodic_memory"):
            agent.episodic_memory.store({
                "type": "emotional_state",
                "timestamp": timestamp,
                "state": self.current_emotional_state.copy()
            })
        
        return True

    def _show_empathy(self, agent, target_state: dict) -> bool:
        """Generate empathetic responses based on target's emotional state."""
        empathy_templates = {
            "joy": "I'm really happy for you! {response}",
            "sadness": "I understand this is difficult. {response}",
            "anger": "I can see why you'd feel that way. {response}",
            "fear": "It's natural to feel concerned. {response}",
            "surprise": "That must have been unexpected! {response}",
            "trust": "I appreciate your confidence. {response}"
        }
        
        if "emotion" in target_state and target_state["emotion"] in empathy_templates:
            response = self._generate_empathetic_response(target_state)
            template = empathy_templates[target_state["emotion"]]
            
            # Store the empathetic interaction
            if hasattr(agent, "episodic_memory"):
                agent.episodic_memory.store({
                    "type": "empathy_response",
                    "target_emotion": target_state["emotion"],
                    "response": template.format(response=response),
                    "timestamp": datetime.datetime.now().isoformat()
                })
            
            return True
        return False

    def _generate_empathetic_response(self, target_state: dict) -> str:
        """Generate an appropriate empathetic response based on the target's emotional state."""
        responses = {
            "joy": ["That's wonderful to hear!", "Your happiness is contagious!"],
            "sadness": ["I'm here to listen", "Take all the time you need"],
            "anger": ["That sounds really frustrating", "I understand your feelings"],
            "fear": ["Let's work through this together", "You're not alone in this"],
            "surprise": ["What an unexpected turn!", "That's quite remarkable!"],
            "trust": ["I value your confidence", "Thank you for sharing that"]
        }
        
        emotion = target_state.get("emotion", "neutral")
        intensity = target_state.get("intensity", 0.5)
        
        if emotion in responses:
            # Select response based on emotion and intensity
            response_options = responses[emotion]
            response_index = min(int(intensity * len(response_options)), len(response_options) - 1)
            return response_options[response_index]
        
        return "I understand"

    def actions_definitions_prompt(self) -> str:
        return """
        You can perform the following emotional intelligence actions:
        - ANALYZE_EMOTION: Analyze the emotional content of a message or situation
        - REGULATE_EMOTION: Apply emotional regulation strategies (reappraisal, suppression, acceptance)
        - SHOW_EMPATHY: Generate empathetic responses to others' emotions
        - UPDATE_EMOTIONAL_STATE: Update your current emotional state
        """

    def actions_constraints_prompt(self) -> str:
        return """
        When using emotional intelligence actions:
        - ANALYZE_EMOTION must include detailed text content to analyze
        - REGULATE_EMOTION must specify a valid regulation strategy (reappraisal, suppression, acceptance)
        - SHOW_EMPATHY must include the target's emotional state and intensity
        - UPDATE_EMOTIONAL_STATE must include valid emotional dimensions (valence, arousal, dominance)
        """

class AdvancedReasoningFaculty(TinyMentalFaculty):
    """Provides advanced reasoning capabilities including:
    - Causal reasoning
    - Analogical thinking
    - Hypothesis generation and testing
    - Decision making
    - Problem solving
    """
    
    def __init__(self):
        super().__init__("Advanced Reasoning")
        self.reasoning_context = []
        self.decision_history = []
        self.hypothesis_log = []
        
    def process_action(self, agent, action: dict) -> bool:
        """Process advanced reasoning actions."""
        action_handlers = {
            "ANALYZE_CAUSALITY": self._analyze_causality,
            "GENERATE_ANALOGY": self._generate_analogy,
            "FORM_HYPOTHESIS": self._form_hypothesis,
            "MAKE_DECISION": self._make_decision,
            "SOLVE_PROBLEM": self._solve_problem
        }
        
        if action["type"] in action_handlers:
            return action_handlers[action["type"]](agent, action["content"])
        return False

    def _analyze_causality(self, agent, situation: dict) -> bool:
        """Analyze cause-effect relationships in a given situation."""
        analysis = {
            "situation": situation["description"],
            "causes": self._identify_causes(situation["context"]),
            "effects": self._predict_effects(situation["context"]),
            "confidence": self._calculate_confidence(situation["evidence"]),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.reasoning_context.append(analysis)
        
        if hasattr(agent, "episodic_memory"):
            agent.episodic_memory.store({
                "type": "causal_analysis",
                "analysis": analysis
            })
        
        return True

    def _generate_analogy(self, agent, concept: dict) -> bool:
        """Create analogies to explain complex concepts."""
        analogy = {
            "source_domain": concept["topic"],
            "target_domain": self._find_analogous_domain(concept["topic"]),
            "mappings": self._create_mappings(concept["attributes"]),
            "explanation": self._generate_analogy_explanation(concept),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.reasoning_context.append(analogy)
        
        if hasattr(agent, "episodic_memory"):
            agent.episodic_memory.store({
                "type": "analogy_generation",
                "analogy": analogy
            })
        
        return True

    def _form_hypothesis(self, agent, observation: dict) -> bool:
        """Generate and test hypotheses based on observations."""
        hypothesis = {
            "observation": observation["data"],
            "hypothesis": self._generate_hypothesis(observation["context"]),
            "predictions": self._make_predictions(observation["context"]),
            "test_criteria": self._define_test_criteria(observation["context"]),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.hypothesis_log.append(hypothesis)
        
        if hasattr(agent, "episodic_memory"):
            agent.episodic_memory.store({
                "type": "hypothesis_formation",
                "hypothesis": hypothesis
            })
        
        return True

    def _make_decision(self, agent, situation: dict) -> bool:
        """Make decisions based on available information and goals."""
        decision = {
            "context": situation["context"],
            "options": situation["options"],
            "criteria": self._evaluate_criteria(situation["constraints"]),
            "choice": self._select_best_option(situation["options"], situation["constraints"]),
            "rationale": self._generate_decision_rationale(situation),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.decision_history.append(decision)
        
        if hasattr(agent, "episodic_memory"):
            agent.episodic_memory.store({
                "type": "decision_making",
                "decision": decision
            })
        
        return True

    def _solve_problem(self, agent, problem: dict) -> bool:
        """Apply problem-solving strategies to find solutions."""
        solution = {
            "problem": problem["description"],
            "approach": self._determine_approach(problem["type"]),
            "steps": self._generate_solution_steps(problem["context"]),
            "outcome": self._evaluate_solution(problem["constraints"]),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.reasoning_context.append(solution)
        
        if hasattr(agent, "episodic_memory"):
            agent.episodic_memory.store({
                "type": "problem_solving",
                "solution": solution
            })
        
        return True

    def actions_definitions_prompt(self) -> str:
        return """
        You can perform the following advanced reasoning actions:
        - ANALYZE_CAUSALITY: Analyze cause-effect relationships in situations
        - GENERATE_ANALOGY: Create analogies to explain complex concepts
        - FORM_HYPOTHESIS: Generate and test hypotheses based on observations
        - MAKE_DECISION: Make informed decisions based on available information
        - SOLVE_PROBLEM: Apply problem-solving strategies to find solutions
        """

    def actions_constraints_prompt(self) -> str:
        return """
        When using advanced reasoning actions:
        - ANALYZE_CAUSALITY must include situation description and context
        - GENERATE_ANALOGY must specify the concept and desired attributes
        - FORM_HYPOTHESIS must provide observation data and context
        - MAKE_DECISION must include options and constraints
        - SOLVE_PROBLEM must describe the problem and any constraints
        """

    # Helper methods for causality analysis
    def _identify_causes(self, context: str) -> list:
        """Identify potential causes in the given context."""
        # Implementation would analyze context for causal factors
        return []

    def _predict_effects(self, context: str) -> list:
        """Predict potential effects based on the context."""
        # Implementation would predict likely outcomes
        return []

    def _calculate_confidence(self, evidence: list) -> float:
        """Calculate confidence level in the causal analysis."""
        # Implementation would evaluate evidence strength
        return 0.0

    # Helper methods for analogy generation
    def _find_analogous_domain(self, topic: str) -> str:
        """Find an appropriate analogous domain for the topic."""
        # Implementation would select relevant analogy domain
        return ""

    def _create_mappings(self, attributes: list) -> dict:
        """Create mappings between source and target domains."""
        # Implementation would establish analogical mappings
        return {}

    def _generate_analogy_explanation(self, concept: dict) -> str:
        """Generate a clear explanation of the analogy."""
        # Implementation would create explanation
        return ""

    # Helper methods for decision making
    def _evaluate_criteria(self, constraints: list) -> list:
        """Evaluate decision criteria based on constraints."""
        # Implementation would assess decision criteria
        return []

    def _select_best_option(self, options: list, constraints: list) -> str:
        """Select the best option based on criteria and constraints."""
        # Implementation would choose optimal option
        return ""

    def _generate_decision_rationale(self, situation: dict) -> str:
        """Generate explanation for the decision."""
        # Implementation would explain decision logic
        return ""

    # Helper methods for problem solving
    def _determine_approach(self, problem_type: str) -> str:
        """Determine the best problem-solving approach."""
        # Implementation would select problem-solving strategy
        return ""

    def _generate_solution_steps(self, context: str) -> list:
        """Generate steps to solve the problem."""
        # Implementation would create solution plan
        return []

    def _evaluate_solution(self, constraints: list) -> dict:
        """Evaluate the proposed solution against constraints."""
        # Implementation would assess solution validity
        return {}

class SpecializedSkillsFaculty(TinyMentalFaculty):
    """
    Provides domain-specific skills and expertise.
    Skills can be dynamically loaded based on the agent's role.
    """
    
    def __init__(self, skills: List[str] = None):
        super().__init__("Specialized Skills")
        self.skills = skills or []
        self.skill_levels = {}
        
    def process_action(self, agent, action: dict) -> bool:
        if action["type"] == "USE_SKILL":
            return self._use_skill(agent, action["skill"], action["parameters"])
        elif action["type"] == "LEARN_SKILL":
            return self._learn_skill(agent, action["skill"])
        elif action["type"] == "ASSESS_EXPERTISE":
            return self._assess_expertise(agent, action["skill"])
        return False

    def _use_skill(self, agent, skill: str, parameters: dict) -> bool:
        if skill in self.skills:
            # Implementation would apply the skill
            return True
        return False

    def _learn_skill(self, agent, skill: str) -> bool:
        if skill not in self.skills:
            self.skills.append(skill)
            self.skill_levels[skill] = 0.1  # Initial skill level
        return True

    def _assess_expertise(self, agent, skill: str) -> bool:
        # Implementation would evaluate current expertise level
        return True

    def actions_definitions_prompt(self) -> str:
        return """
        The agent can perform the following skill-related actions:
        - USE_SKILL: Apply a learned skill to a situation
        - LEARN_SKILL: Acquire a new skill or improve existing one
        - ASSESS_EXPERTISE: Evaluate current expertise level
        """

class CreativityFaculty(TinyMentalFaculty):
    """
    Provides creative thinking and innovation capabilities.
    """
    
    def __init__(self):
        super().__init__("Creativity")
        self.inspiration_sources = []
        
    def process_action(self, agent, action: dict) -> bool:
        if action["type"] == "BRAINSTORM":
            return self._brainstorm(agent, action["topic"])
        elif action["type"] == "COMBINE_IDEAS":
            return self._combine_ideas(agent, action["ideas"])
        elif action["type"] == "EVALUATE_NOVELTY":
            return self._evaluate_novelty(agent, action["idea"])
        return False

    def _brainstorm(self, agent, topic: str) -> bool:
        # Implementation would generate creative ideas
        return True

    def _combine_ideas(self, agent, ideas: List[str]) -> bool:
        # Implementation would synthesize new ideas
        return True

    def _evaluate_novelty(self, agent, idea: str) -> bool:
        # Implementation would assess idea originality
        return True

    def actions_definitions_prompt(self) -> str:
        return """
        The agent can perform the following creative actions:
        - BRAINSTORM: Generate multiple ideas on a topic
        - COMBINE_IDEAS: Synthesize new ideas from existing ones
        - EVALUATE_NOVELTY: Assess the originality of ideas
        """
