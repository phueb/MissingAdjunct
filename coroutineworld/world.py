import random
from typing import Generator, Union

from coroutineworld import configs
from coroutineworld.state import State
from coroutineworld.communications import Query, TICK, TOCK
from coroutineworld.entity import Animate, InAnimate

from semantics.entities import animates, inanimates


class World(object):
    def __init__(self):
        self.num_x = configs.World.num_x
        self.num_y = configs.World.num_y
        self.xy2state = {}

        # populate each cell
        for x in range(self.num_x):
            for y in range(self.num_y):
                animates_ = [InAnimate.from_def(a_def) for a_def in
                             random.choices(animates.definitions, k=configs.World.num_animates_per_cell)]
                inanimates_ = [InAnimate.from_def(a_def) for a_def in
                               random.choices(inanimates.definitions, k=configs.World.num_inanimates_per_cell)]
                self.xy2state[(x, y)] = State(animates=animates_,
                                              inanimates=inanimates_)

    def query(self, x, y):
        return self.xy2state[(x % self.num_x, y % self.num_y)]

    def turn(self, interface: Generator[Union[TICK, TOCK], State, None]):

        comm = next(interface)
        while comm is not TICK:

            # communication from semantic rules to world
            if isinstance(comm, Query):
                state = self.query(comm.x, comm.y)
                comm = interface.send(state)

            # communication from world to semantic rules
            elif comm is TOCK:
                comm = next(interface)

            else:
                raise RuntimeError(f'Did not recognize {comm}')

    def __str__(self):
        res = 'World states:\n'
        for (x, y), state in self.xy2state.items():
            res += f'{x} {y} | {state}\n'
        return res
