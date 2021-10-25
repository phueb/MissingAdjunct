from dataclasses import dataclass
from typing import List

from coroutineworld.entity import Entity, Animate, InAnimate


@dataclass
class State:
    animates: List[Animate]
    inanimates: List[InAnimate]

    def __str__(self):
        return f'State with {len(self.animates):>3} animates and {len(self.inanimates):>3} inanimates'

    def has_name(self, entity: Entity) -> bool:
        for ie in self.inanimates:
            if ie.name == entity.name:
                return True
        for ae in self.animates:
            if ae.name == entity.name:
                return True
        return False

