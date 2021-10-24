from typing import Coroutine

from coroutineworld.communications import Query
from coroutineworld.state import State


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