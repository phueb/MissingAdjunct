"""
This file defines what primitives are triggered by each verb.
"""

from coroutineworld.primitives import MoveIfY
from coroutineworld.event import Action
from coroutineworld import configs

T = True
F = False

verb2action = {

    'look_for': Action(
        name='look_for',
        primitives=[
            MoveIfY()
        ],
        failure_probability=configs.Action.failure_probability,
        num_attempts=10,
        requires_x=T,
        requires_y=T,
        requires_i=F,
        requires_l=F,
    ),

    'eat': Action(
        name='eat',
        primitives=[
        ],
        failure_probability=configs.Action.failure_probability,
        num_attempts=10,
        requires_x=T,
        requires_y=T,
        requires_i=F,
        requires_l=F,
    ),


}
