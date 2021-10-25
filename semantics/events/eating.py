"""
Event sequences are an ordered list of actions that end with an eating action.
There may be multiple sequences that are legal for a given entity.
Sequences are differentiated by who is eating: This can be a category of entities, or specific members.


Arguments to verbs are X, Y, Z, always in this order.
What types these variables refer to must be documented in lexicon.py

"""

from coroutineworld.load import LoadEntity
from coroutineworld.event import Event
from coroutineworld.entity import Animate, InAnimate

from semantics.verbs import verb2action


entity2eat_events = {

    # HUMANS

    'Mary': (
        Event(
            requirements_y={
                'look_for': [
                    LoadEntity(cls=InAnimate, name='strawberry'),
                ],
            },
            likelihood=1,
            actions=[
                verb2action['look_for'],
                verb2action['eat'],
            ],
        ),
    ),

    'John': (
        Event(
            requirements_y={
                'look_for': [
                    LoadEntity(cls=InAnimate, name='strawberry'),
                ],
            },
            likelihood=1,
            actions=[
                verb2action['look_for'],
                verb2action['eat'],
            ],
        ),
    ),

    'squirrel': (
        Event(
            requirements_y={
                'look_for': [
                    LoadEntity(cls=InAnimate, name='acorn'),
                ],
            },
            likelihood=1,
            actions=[
                verb2action['look_for'],
                verb2action['eat'],
            ],
        ),
    ),



}
