import colorlog
from typing import Coroutine

from coroutineworld.state import State
from coroutineworld.entity import Animate
from coroutineworld.communications import Query


class Primitive:
    def __call__(self,
                 x: int,
                 y: int,
                 state: State,
                 animate: Animate,
                 ) -> Coroutine[Query, None, bool]:
        raise NotImplementedError


class MoveIfY(Primitive):
    def __init__(self,
                 ):
        pass

    def __call__(self,
                 x: int,
                 y: int,
                 state: State,
                 animate: Animate,
                 ) -> Coroutine[Query, None, bool]:
        raise NotImplementedError







