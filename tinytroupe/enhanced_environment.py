"""
Enhanced environment system for TinyTroupe.
Provides improved environment simulation including physical space,
time management, and event handling.
"""

from typing import Any, Dict, List, Optional, Tuple
import datetime
import logging
import json
from dataclasses import dataclass
from collections import defaultdict

from tinytroupe.environment import TinyWorld
from tinytroupe.agent import TinyPerson

logger = logging.getLogger("tinytroupe")

@dataclass
class Location:
    """Represents a physical location in the environment."""
    name: str
    coordinates: Tuple[float, float]  # (x, y) coordinates
    type: str  # e.g., "room", "building", "outdoor"
    properties: Dict[str, Any]  # Additional properties like size, capacity, etc.
    connected_to: List[str]  # Names of connected locations

@dataclass
class EnvironmentEvent:
    """Represents an event in the environment."""
    name: str
    start_time: datetime.datetime
    duration: datetime.timedelta
    location: str
    participants: List[str]
    properties: Dict[str, Any]

class PhysicalEnvironment(TinyWorld):
    """
    Enhanced environment with physical space simulation.
    """
    
    def __init__(self, name: str = "Physical Environment"):
        super().__init__(name)
        self.locations: Dict[str, Location] = {}
        self.agent_locations: Dict[str, str] = {}  # agent_name -> location_name
        self.events: List[EnvironmentEvent] = []
        
    def add_location(self, location: Location) -> None:
        """Add a new location to the environment."""
        self.locations[location.name] = location
        
    def move_agent(self, agent: TinyPerson, target_location: str) -> bool:
        """Move an agent to a new location."""
        if target_location not in self.locations:
            return False
            
        current_location = self.agent_locations.get(agent.name)
        if current_location:
            # Check if movement is possible
            if target_location not in self.locations[current_location].connected_to:
                return False
                
        self.agent_locations[agent.name] = target_location
        # Update agent's context with new location
        agent.change_context([f"Location: {target_location}"])
        return True
        
    def get_nearby_agents(self, agent: TinyPerson, radius: float = 1.0) -> List[TinyPerson]:
        """Get agents within a certain radius of the given agent."""
        agent_location = self.agent_locations.get(agent.name)
        if not agent_location:
            return []
            
        nearby_agents = []
        agent_coords = self.locations[agent_location].coordinates
        
        for other_agent_name, other_location in self.agent_locations.items():
            if other_agent_name == agent.name:
                continue
                
            other_coords = self.locations[other_location].coordinates
            distance = ((agent_coords[0] - other_coords[0])**2 + 
                       (agent_coords[1] - other_coords[1])**2)**0.5
                       
            if distance <= radius:
                other_agent = TinyPerson.get_agent_by_name(other_agent_name)
                if other_agent:
                    nearby_agents.append(other_agent)
                    
        return nearby_agents

class TimeAwareEnvironment(TinyWorld):
    """
    Environment with enhanced time management and scheduling.
    """
    
    def __init__(self, name: str = "Time-Aware Environment",
                 start_time: datetime.datetime = None):
        super().__init__(name)
        self.current_time = start_time or datetime.datetime.now()
        self.time_scale = 1.0  # 1.0 means real-time, 2.0 means twice as fast
        self.scheduled_events: List[EnvironmentEvent] = []
        self.recurring_events: Dict[str, datetime.timedelta] = {}
        
    def schedule_event(self, event: EnvironmentEvent) -> None:
        """Schedule a new event."""
        self.scheduled_events.append(event)
        self.scheduled_events.sort(key=lambda x: x.start_time)
        
    def add_recurring_event(self, event: EnvironmentEvent, 
                          interval: datetime.timedelta) -> None:
        """Add a recurring event."""
        self.scheduled_events.append(event)
        self.recurring_events[event.name] = interval
        
    def advance_time(self, delta: datetime.timedelta) -> None:
        """Advance the environment's time."""
        target_time = self.current_time + delta
        
        # Process events that should occur
        while (self.scheduled_events and 
               self.scheduled_events[0].start_time <= target_time):
            event = self.scheduled_events.pop(0)
            self._process_event(event)
            
            # Reschedule if recurring
            if event.name in self.recurring_events:
                next_event = EnvironmentEvent(
                    name=event.name,
                    start_time=event.start_time + self.recurring_events[event.name],
                    duration=event.duration,
                    location=event.location,
                    participants=event.participants,
                    properties=event.properties
                )
                self.schedule_event(next_event)
                
        self.current_time = target_time
        
    def _process_event(self, event: EnvironmentEvent) -> None:
        """Process an event and its effects on the environment."""
        # Notify participants
        for participant_name in event.participants:
            agent = TinyPerson.get_agent_by_name(participant_name)
            if agent:
                agent.socialize(
                    f"Event '{event.name}' is starting at {event.location}",
                    source=self
                )

class HybridEnvironment(PhysicalEnvironment, TimeAwareEnvironment):
    """
    Combined environment with both physical space and time management.
    """
    
    def __init__(self, name: str = "Hybrid Environment",
                 start_time: datetime.datetime = None):
        PhysicalEnvironment.__init__(self, name)
        TimeAwareEnvironment.__init__(self, name, start_time)
        self.location_events: Dict[str, List[EnvironmentEvent]] = defaultdict(list)
        
    def schedule_event(self, event: EnvironmentEvent) -> None:
        """Schedule an event and track its location."""
        super().schedule_event(event)
        self.location_events[event.location].append(event)
        
    def get_location_events(self, location: str,
                          start_time: datetime.datetime = None,
                          end_time: datetime.datetime = None) -> List[EnvironmentEvent]:
        """Get events at a specific location within a time window."""
        events = self.location_events[location]
        if start_time is None and end_time is None:
            return events
            
        filtered_events = []
        for event in events:
            event_end = event.start_time + event.duration
            if start_time and event_end < start_time:
                continue
            if end_time and event.start_time > end_time:
                continue
            filtered_events.append(event)
            
        return filtered_events
        
    def move_agent(self, agent: TinyPerson, target_location: str) -> bool:
        """Move an agent and notify about relevant events."""
        success = super().move_agent(agent, target_location)
        if success:
            # Notify about current and upcoming events
            location_events = self.get_location_events(
                target_location,
                self.current_time,
                self.current_time + datetime.timedelta(hours=1)
            )
            if location_events:
                event_descriptions = []
                for event in location_events:
                    event_descriptions.append(
                        f"Event '{event.name}' at {event.start_time.strftime('%H:%M')}"
                    )
                agent.socialize(
                    f"Events at {target_location}: " + ", ".join(event_descriptions),
                    source=self
                )
        return success
