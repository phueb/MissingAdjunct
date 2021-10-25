from typing import Coroutine, Generator, Union, Dict
import colorlog
from itertools import product
import random

from coroutineworld.world import World
from coroutineworld.state import State
from coroutineworld.communications import Query, TICK, TOCK
from coroutineworld.language import LogicalForm, Corpus
from coroutineworld.event import Event, Action
from coroutineworld.entity import Animate
from coroutineworld.primitives import Primitive, MoveIfY
from coroutineworld import configs

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    fmt='%(log_color)s%(levelname)s:%(name)s:%(message)s',
    log_colors={
        'DEBUG': 'green',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
))

log_main = colorlog.getLogger('main')
log_main.addHandler(handler)
log_main.setLevel('DEBUG')

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

log_language = colorlog.getLogger('language')
log_language.addHandler(handler)
log_language.setLevel('DEBUG')


corpus = Corpus()


def modify_state(x: int,
                 y: int,
                 ) -> Coroutine[Query, State, None]:
    """modify the state of a cell in the world"""

    # get state of current cell
    state_current = yield Query(x, y)

    animate2state_src: Dict[Animate, State] = {}

    # check neighboring cells (north, south, east, west)
    for xs, ys in product([0, 1], [0, 1]):
        state_neighbor = yield Query(x + xs, y + ys)

        for animate in state_neighbor.animates:

            log_main.info('\n')

            # decide event
            drive = animate.get_max_drive()
            event = animate.decide_event(drive)

            event_failed = False

            # perform all actions
            for action in event.actions:
                action: Action

                # get optional requirements for action
                try:
                    requirements_y = event.requirements_y[action.name]
                except KeyError:
                    entity_y = None
                else:
                    entity_y = random.choice(requirements_y)()

                # perform all primitives of action
                for primitive in action.primitives:

                    # move animate entity to current cell if current cell if condition is met
                    if isinstance(primitive, MoveIfY):
                        if state_current.has_name(entity_y.name):
                            log_main.debug(f'{animate} moved to {x} {y}')
                            animate2state_src[animate] = state_neighbor
                        else:
                            log_main.debug(f'{animate} did not move to {x} {y}')
                            event_failed = True
                    else:
                        raise NotImplementedError

                # update drives
                animate.hunger.up()

                if event_failed:
                    log_main.warning(f'{event} failed')
                    break

                # linguistic description
                lf = LogicalForm(x=animate.name, v=action.name, y=entity_y)
                corpus.logical_forms.append(lf)
                log_language.info(corpus.to_sentence(lf))

            if not event_failed:
                drive.reset()

    # now move animate entities - do not move entities while iterating over them
    for animate, state_src in animate2state_src.items():
        state_src.animates.remove(animate)
        state_current.animates.append(animate)

    yield TOCK


def get_interface() -> Generator[Union[TICK, TOCK], State, None]:
    """
    enable 2-way communication between world and semantic rules that drive it
    """

    while True:
        for y in range(configs.World.num_x):
            for x in range(configs.World.num_y):
                yield from modify_state(x, y)

        yield TICK


def main():

    world = World()  # a grid where each cell has a state
    interface = get_interface()  # interface that enables 2-way communications between world and semantic rules

    log_main.info(world)

    for i in range(configs.World.num_turns):

        log_main.info('=' * 40)
        log_main.info(f'turn ={i}')

        world.turn(interface)
        log_main.info(world)


if __name__ == '__main__':

    main()
