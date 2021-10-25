import colorlog
from typing import Coroutine

from coroutineworld.state import State
from coroutineworld.entity import Animate
from coroutineworld.communications import Query


handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    fmt='%(log_color)s%(levelname)s:%(name)s:%(message)s',
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'blue',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
))

log_primitives = colorlog.getLogger('primitives')
log_primitives.addHandler(handler)
log_primitives.setLevel('DEBUG')


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







