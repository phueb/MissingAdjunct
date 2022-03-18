from dataclasses import dataclass
from typing import Tuple, Optional

LOC1 = 'kitchen'
LOC2 = 'workshop'


@dataclass
class LogicalForm:
    agent: str
    verb: str
    theme: str
    instrument: Optional[str]
    location: Optional[str]

    verb_type: int
    epoch: int


@dataclass
class Verb:
    """a control verb with only 1 instrument"""

    type: int
    name: str
    instrument: Optional[str]

    def __post_init__(self):
        if self.type in {2, 3} and self.instrument is None:
            raise AttributeError('Type 2 and 3 verbs require 1 instrument')


@dataclass
class Agent:
    names: Tuple[str, str, str]
    location: Optional[str]


@dataclass
class Theme:
    category: str
    names: Tuple[str, str, str]
    verbs: Tuple[Verb, Verb, Verb, Verb]
    location: str


agent_classes = (
    Agent(names=('John', 'Mary', 'Fatima'),
          location=None,
          ),
    Agent(names=('cook', 'chef', 'baker'),
          location=LOC1,
          ),
    Agent(names=('craftsman', 'builder', 'technician'),
          location=LOC2,
          ),
)


theme_classes = (

    # LOCATION 1 #########################################################

    Theme(category='VEGETABLE',
          names=('potato', 'cucumber', 'pepper'),
          verbs=(Verb(type=0, name='dice', instrument=None),
                 Verb(type=1, name='ferment', instrument=None),
                 Verb(type=2, name='grow', instrument='fertilizer'),
                 Verb(type=3, name='preserve', instrument='vinegar'),
                 ),
          location=LOC1
          ),

    Theme(category='FRUIT',
          names=('strawberry', 'raspberry', 'orange'),
          verbs=(Verb(type=0, name='dice', instrument=None),
                 Verb(type=1, name='pick', instrument=None),
                 Verb(type=2, name='spray', instrument='insecticide'),
                 Verb(type=3, name='preserve', instrument='dehydrator'),
                 ),
          location=LOC1
          ),

    Theme(category='APPLIANCE',
          names=('fridge', 'microwave', 'blender'),
          verbs=(Verb(type=0, name='disinfect', instrument=None),
                 Verb(type=1, name='supply', instrument=None),
                 Verb(type=2, name='fill', instrument='food'),
                 Verb(type=3, name='repair', instrument='wrench'),
                 ),
          location=LOC1
          ),

    Theme(category='KITCHENWARE',
          names=('plate', 'cup', 'bowl'),
          verbs=(Verb(type=0, name='disinfect', instrument=None),
                 Verb(type=1, name='wash', instrument=None),
                 Verb(type=2, name='organize', instrument='organizer'),
                 Verb(type=3, name='repair', instrument='glue')
                 ),
          location=LOC1
          ),

    Theme(category='JUICE',
          names=('orange-juice', 'apple-juice', 'tomato-juice'),
          verbs=(Verb(type=0, name='taste', instrument=None),
                 Verb(type=1, name='drink', instrument=None),
                 Verb(type=2, name='freeze', instrument='freezer'),
                 Verb(type=3, name='pour', instrument='pitcher'),
                 ),
          location=LOC1
          ),

    Theme(category='DESERT',
          names=('pudding', 'pie', 'cookie'),
          verbs=(Verb(type=0, name='taste', instrument=None),
                 Verb(type=1, name='eat', instrument=None),
                 Verb(type=2, name='consume', instrument='utensil'),
                 Verb(type=3, name='decorate', instrument='icing'),
                 ),
          location=LOC1
          ),

    Theme(category='FOWL',
          names=('chicken', 'duck', 'turkey'),
          verbs=(Verb(type=0, name='season', instrument=None),
                 Verb(type=1, name='refrigerate', instrument=None),
                 Verb(type=2, name='grill', instrument='bbq'),
                 Verb(type=3, name='carve', instrument='knife'),
                 ),
          location=LOC1
          ),

    Theme(category='FISH',
          names=('salmon', 'trout', 'tilapia'),
          verbs=(Verb(type=0, name='season', instrument=None),
                 Verb(type=1, name='fry', instrument=None),
                 Verb(type=2, name='catch', instrument='net'),
                 Verb(type=3, name='heat', instrument='oven'),
                 ),
          location=LOC1
          ),

    # LOCATION 2 #########################################################

    Theme(category='CLOTH',
          names=('shirt', 'pants', 'sock'),
          verbs=(Verb(type=0, name='store', instrument=None),
                 Verb(type=1, name='fold', instrument=None),
                 Verb(type=2, name='dry', instrument='dryer'),
                 Verb(type=3, name='cut', instrument='scissors'),
                 ),
          location=LOC2
          ),

    Theme(category='WOOD',
          names=('pine', 'mahogany', 'ash'),
          verbs=(Verb(type=0, name='store', instrument=None),
                 Verb(type=1, name='sand', instrument=None),
                 Verb(type=2, name='seal', instrument='lacquer'),
                 Verb(type=3, name='cut', instrument='saw'),
                 ),
          location=LOC2
          ),

    Theme(category='PPE',
          names=('goggles', 'glove', 'faceshield'),
          verbs=(Verb(type=0, name='inspect', instrument=None),
                 Verb(type=1, name='reuse', instrument=None),
                 Verb(type=2, name='dust', instrument='duster'),
                 Verb(type=3, name='clean', instrument='towel'),
                 ),
          location=LOC2
          ),

    Theme(category='MACHINERY',
          names=('tablesaw', 'beltsander', 'workstation'),
          verbs=(Verb(type=0, name='inspect', instrument=None),
                 Verb(type=1, name='install', instrument=None),
                 Verb(type=2, name='lubricate', instrument='lubricant'),
                 Verb(type=3, name='clean', instrument='vacuum'),
                 ),
          location=LOC2
          ),

    Theme(category='GASOLINE',
          names=('coolant', 'anti-freeze', 'brake-fluid'),
          verbs=(Verb(type=0, name='buy', instrument=None),
                 Verb(type=1, name='siphon', instrument=None),
                 Verb(type=2, name='transfer', instrument='pump'),
                 Verb(type=3, name='pour', instrument='canister'),
                 ),
          location=LOC2
          ),

    Theme(category='CAR',
          names=('car', 'truck', 'motorcycle'),
          verbs=(Verb(type=0, name='buy', instrument=None),
                 Verb(type=1, name='drive', instrument=None),
                 Verb(type=2, name='polish', instrument='polisher'),
                 Verb(type=3, name='decorate', instrument='paint'),
                 ),
          location=LOC2
          ),

    Theme(category='ROCK',
          names=('granite', 'limestone', 'marble'),
          verbs=(Verb(type=0, name='collect', instrument=None),
                 Verb(type=1, name='crush', instrument=None),
                 Verb(type=2, name='shoot', instrument='slingshot'),
                 Verb(type=3, name='carve', instrument='chisel'),
                 ),
          location=LOC2
          ),

    Theme(category='METAL',
          names=('iron', 'steel', 'copper'),
          verbs=(Verb(type=0, name='collect', instrument=None),
                 Verb(type=1, name='melt', instrument=None),
                 Verb(type=2, name='harden', instrument='hammer'),
                 Verb(type=3, name='heat', instrument='furnace'),
                 ),
          location=LOC2
          ),

)
experimental_themes = ['pepper',
                       'orange',
                       'blender',
                       'bowl',
                       'tomato-juice',
                       'cookie',
                       'turkey',
                       'tilapia',
                       'sock',
                       'ash',
                       'faceshield',
                       'workstation',
                       'brake-fluid',
                       'motorcycle',
                       'marble',
                       'copper',
                       ]