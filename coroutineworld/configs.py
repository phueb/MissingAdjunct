

class World:

    num_x = 8
    num_y = 8

    num_turns = 2

    num_animates_per_cell = 1
    num_inanimates_per_cell = 1


class Language:
    location_probability: float = 0.5
    instrument_probability: float = 0.5


class Action:
    failure_probability = 0.0
