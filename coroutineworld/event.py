"""
An event consists of a sequence of actions that result in the reduction of one drive
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple, Union, Type

from coroutineworld.load import LoadEntity
from coroutineworld.primitives import Primitive


@dataclass
class Action:
    name: str
    primitives: List[Primitive]
    failure_probability: float
    num_attempts: int
    requires_x: bool = False  # agent
    requires_y: bool = False  # theme/patient
    requires_l: bool = False  # location
    requires_i: bool = False  # instrument

    def __str__(self):
        return f'"{self.name}"'


@dataclass
class Event:
    actions: List[Action]
    likelihood: int  # between 1 and 10

    requirements_y: Dict[str, List[LoadEntity]]
    requirements_i: Dict[str, List[LoadEntity]] = field(default_factory=dict)
    requirements_l: Dict[str, List[LoadEntity]] = field(default_factory=dict)

    def __str__(self):
        return f'<Event {self.actions[-1]}>'
