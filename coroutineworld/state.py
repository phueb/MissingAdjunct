from dataclasses import dataclass
from typing import List

from coroutineworld.entity import Entity


@dataclass
class State:
    region: str
    entities: List[Entity]

    def __str__(self):
        return f'State with {len(self.entities):>3} entities'


