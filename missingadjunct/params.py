from dataclasses import dataclass


@dataclass
class Params:
    num_epochs: int
    include_location: bool
    include_location_specific_agents: bool
