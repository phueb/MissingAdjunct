import random
from typing import Optional, Dict, List, Type
from dataclasses import dataclass

from coroutineworld.drives import Hunger, Thirst, Fatigue, Drive


class Entity:
    def __init__(self,
                 name: str,
                 categories: List[str],
                 **kwargs
                 ):
        self.name = name
        self.categories = categories
        self.definite = False  # todo how does an entity become definite?

    def __str__(self):
        res = f'<Entity name={self.name}>'
        return res

    def __repr__(self):
        """this string will show when entity is printed as part of a collection (e.g. inside a list)"""
        return self.name

    @classmethod
    def from_def(cls,
                 d,  # of type EntityDef
                 entity_kwargs: Optional[Dict] = None,
                 ):
        if entity_kwargs:
            return d.cls(**d.__dict__, **entity_kwargs)
        else:
            return d.cls(**d.__dict__)


@dataclass
class EntityDefinition:
    name: str
    categories: List[str]  # top-most category first,
    cls: Type[Entity]

    # todo what about custom attributes?


class InAnimate(Entity):
    def __init__(self,
                 name: str,
                 categories: List[str],
                 **kwargs
                 ):
        super().__init__(name, categories, **kwargs)

        kwargs.pop('cls')


class Animate(Entity):
    def __init__(self,
                 name: str,
                 categories: List[str],
                 **kwargs,
                 ):
        super().__init__(name, categories, **kwargs)

        kwargs.pop('cls')

        self.hunger = Hunger()
        self.thirst = Thirst()
        self.fatigue = Fatigue()

    @property
    def is_animate(self):
        return True

    def get_max_drive(self) -> Drive:

        max_drive = self.hunger  # hunger is the default event type if other drives are equal
        max_level = 0
        for drive in [self.hunger, self.thirst, self.fatigue]:
            if drive.level > max_level:
                max_drive = drive
                max_level = drive.level

        return max_drive

    def decide_event(self,
                     max_drive: Optional[Drive] = None):

        if max_drive is None:
            event_type = self.get_max_drive()
        else:
            event_type = max_drive.event_type

        if event_type == 'eating':
            from semantics.events import eating
            # get one eating sequence
            try:
                events = eating.entity2eat_events[self.name]
            except KeyError:
                raise KeyError(f'{self.name} does not have any "{event_type}" event.')
            else:
                event = random.choices(events, weights=[s.likelihood for s in events])[0]

        else:
            raise NotImplementedError

        from coroutineworld.event import Event
        event: Event

        return event
