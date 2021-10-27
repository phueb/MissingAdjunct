from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Union

LOC1 = 'KITCHEN'
LOC2 = 'WORKSHOP'


@dataclass
class LogicalForm:
    agent: str
    verb: str
    theme: str
    instrument: Optional[str]
    location: Optional[str]


@dataclass
class Verb:
    type: int
    name: str
    instruments: Optional[Dict[Union[LOC1, LOC2], str]]

    def __post_init__(self):
        if self.type in {2, 3} and not isinstance(self.instruments, dict):
            raise AttributeError('Type 2 and 3 verbs must be supplied with dict specifying instrument(s).')
        if self.type == 2 and not (LOC1 in self.instruments or LOC2 in self.instruments):
            raise AttributeError('Verb requires instrument dict with keys matching 1 known location')
        if self.type == 3 and not (LOC1 in self.instruments and LOC2 in self.instruments):
            raise AttributeError('Verb requires instrument dict with keys matching one of 2 known locations')


@dataclass
class Agent:
    members: Tuple[str, str, str]
    location: Optional[str]


@dataclass
class Theme:
    category: str
    members: Tuple[str, str, str]
    verbs: Tuple[Verb, Verb, Verb, Verb]
    location: str


agents = (
    Agent(members=('John', 'Mary', 'Fatima'),
          location=None,
          ),
    Agent(members=('cook', 'chef', 'baker'),
          location=LOC1,
          ),
    Agent(members=('craftsman', 'builder', 'technician'),
          location=LOC2,
          ),
)


themes = (
    Theme(category='DESERT',
          members=('pudding', 'pie', 'cookie'),
          verbs=(Verb(type=0, name='spoon', instruments=None),
                 Verb(type=1, name='eat', instruments=None),
                 Verb(type=2, name='consume', instruments={LOC1: 'utensil'}),
                 Verb(type=3, name='decorate', instruments={LOC1: 'icing', LOC2: 'paint'}),
                 ),
          location=LOC1
          ),

    Theme(category='JUICE',
          members=('orange-juice', 'apple-juice', 'tomato-juice'),
          verbs=(Verb(type=0, name='spoon', instruments=None),
                 Verb(type=1, name='drink', instruments=None),
                 Verb(type=2, name='freeze', instruments={LOC1: 'freezer'}),
                 Verb(type=3, name='consume', instruments={LOC1: 'pitcher', LOC2: 'canister'}),
                 ),
          location=LOC1
          ),
)

