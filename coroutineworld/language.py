from dataclasses import dataclass
from typing import List, Optional

from coroutineworld.entity import Entity


@dataclass
class LogicalForm:
    x: Entity
    v: str
    y: Optional[Entity] = None
    i: Optional[Entity] = None
    l: Optional[Entity] = None


WS = ' '


class Corpus:
    def __init__(self):
        self.logical_forms: List[LogicalForm] = []

    @staticmethod
    def to_sentence(lf: LogicalForm,
                    ) -> str:
        res = f'{lf.x} {lf.v}'

        if lf.y is not None:
            res += WS + lf.y.name

        return res
