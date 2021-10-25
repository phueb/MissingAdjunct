from typing import Union, Type

from coroutineworld.entity import Animate, InAnimate

from semantics.entities.inanimates import definitions as definitions_ie
from semantics.entities.animates import definitions as definitions_ae


class LoadEntity:
    def __init__(self,
                 cls: Union[Type[Animate], Type[InAnimate]],
                 name: str,
                 ):
        self.cls = cls
        self.name = name

    def __call__(self):

        if self.cls == Animate:
            definitions = definitions_ae
        elif self.cls == InAnimate:
            definitions = definitions_ie
        else:
            raise AttributeError

        for definition in definitions:
            if definition.name == self.name:
                return self.cls.from_def(definition)

        else:
            raise RuntimeError(f'Failed to load {self.name}')
