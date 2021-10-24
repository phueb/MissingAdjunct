from dataclasses import dataclass

from coroutineworld.state import State


@dataclass
class Query:
    x: int
    y: int


@dataclass
class Transition:
    x: int
    y: int
    state: State


class TICK:
    pass
