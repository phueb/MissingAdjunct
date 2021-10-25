from dataclasses import dataclass


@dataclass
class Query:
    x: int
    y: int


class TICK:
    def __str__(self):
        return 'TICK'


class TOCK:
    def __str__(self):
        return 'TOCK'
