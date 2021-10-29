from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    pickles = root / 'pickles'


class Corpus:
    num_epochs = 1
    include_location = True
    include_location_specific_agents = True

