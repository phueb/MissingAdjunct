from typing import Coroutine, Generator, Union

from coroutineworld.world import World
from coroutineworld.state import State
from coroutineworld.communications import Query, Transition, TICK
from coroutineworld.semantics import get_next_state, count_neighboring_entities
from coroutineworld import configs


def get_transition(x: int,
                   y: int,
                   ) -> Coroutine[State, Union[Query, int], None]:
    """compute how the state of a cell in the world should transition"""

    state = yield Query(x, y)
    num_neighboring_entities = yield from count_neighboring_entities(x, y)
    next_state = get_next_state(state, num_neighboring_entities)
    yield Transition(x, y, next_state)


def get_interface() -> Generator[None, Union[Transition, TICK], None]:
    """
    enable 2-way communication between world and semantic rules that drive it
    """

    while True:
        for y in range(configs.World.num_x):
            for x in range(configs.World.num_y):
                print(f'x={x} y ={y}')
                yield from get_transition(x, y)
        yield TICK


def main():

    world = World()  # a grid where each cell has a state
    interface = get_interface()  # interface that enables 2-way communications between world and semantic rules

    print(world)

    for i in range(configs.World.num_turns):

        print('--------------------------------------TURN')
        world.turn(interface)
        print(world)


if __name__ == '__main__':

    main()
