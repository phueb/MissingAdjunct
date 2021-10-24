from typing import Coroutine, Generator, Union
from coroutineworld.world import World
from coroutineworld.state import State
from coroutineworld.instructions import Query, Transition, TICK
from coroutineworld.entity import Entity
from coroutineworld import configs


def get_next_state(state: State,
                   num_neighboring_entities: int,
                   ) -> State:

    print(num_neighboring_entities)

    if num_neighboring_entities > 5:
        print(' Updating')
        return State(region=state.region,
                     entities=[
                               ])
    else:
        print(' Not Updating')
    return state


def count_neighboring_entities(y: int,
                               x: int,
                               ) -> Coroutine[State, Query, int]:
    n = yield Query(x + 0, y + 1)  # north
    e = yield Query(x + 1, y + 0)  # east
    s = yield Query(x + 0, y - 1)  # south
    w = yield Query(x - 1, y + 0)  # west

    neighbor_states = [n, e, s, w]
    count = 0
    for state in neighbor_states:
        count += len(state.entities)
    return count


def get_transition(x: int,
                   y: int,
                   ) -> Coroutine[State, Union[Query, int], None]:
    state = yield Query(x, y)
    num_neighboring_entities = yield from count_neighboring_entities(x, y)
    next_state = get_next_state(state, num_neighboring_entities)
    yield Transition(x, y, next_state)


def get_instructions() -> Generator[None, Union[Transition, TICK], None]:
    while True:
        for y in range(configs.World.num_x):
            for x in range(configs.World.num_y):
                print(f'x={x} y ={y}')
                yield from get_transition(x, y)
        yield TICK


def main():
    world = World()  # a grid where each cell has a state
    instructions = get_instructions()  # instructions for how to update the world

    print(world)

    for i in range(configs.World.num_turns):

        print('--------------------------------------TURN')
        world.turn(instructions)
        print(world)


if __name__ == '__main__':

    main()
