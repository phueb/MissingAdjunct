from dataclasses import dataclass, field
from typing import List

i_silent_themes = ['pepper',
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


@dataclass
class Params:
    num_epochs: int
    include_location: bool
    include_location_specific_agents: bool
    instrument_silent_themes: List[str] = field(default_factory=i_silent_themes)
