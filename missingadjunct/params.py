from dataclasses import dataclass
from typing import List


@dataclass
class Params:
    num_epochs: int
    include_location: bool
    include_location_specific_agents: bool
    instrument_silent_themes: List[str]
