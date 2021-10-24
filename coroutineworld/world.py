import random

from coroutineworld import configs
from coroutineworld.state import State
from coroutineworld.communications import Query, Transition, TICK
from coroutineworld.entity import Entity


class World(object):
    def __init__(self):
        self.num_x = configs.World.num_x
        self.num_y = configs.World.num_y
        self.xy2state = {}
        for x, region in enumerate(configs.World.regions):
            for y in range(self.num_y):
                self.xy2state[(x, y)] = State(region=region,
                                              entities=[Entity()
                                                        for _ in range(random.randint(*configs.World.entity_range))],
                                              )

    def query(self, x, y):
        return self.xy2state[(x % self.num_x, y % self.num_y)]

    def assign(self, x, y, state):
        self.xy2state[(x % self.num_x, y % self.num_y)] = state

    def turn(self, interface):

        step = next(interface)
        while step is not TICK:

            # communication from semantic rules to world
            if isinstance(step, Query):
                state = self.query(step.y, step.x)
                step = interface.send(state)

            # communication from world to semantic rules
            elif isinstance(step, Transition):
                self.assign(step.y, step.x, step.state)
                step = next(interface)
            else:
                raise RuntimeError(f'Did not recognize {step}')

    def __str__(self):
        res = ''
        for (x, y), state in self.xy2state.items():
            res += f'{x} {y} | {state}\n'
        return res
