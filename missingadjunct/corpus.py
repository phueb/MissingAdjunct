import pickle
from typing import Optional, Generator, List, Tuple
import datetime
from itertools import product
from functools import lru_cache

from missingadjunct import configs
from missingadjunct.params import Params
from items import LogicalForm, Agent, Theme


FILE_NAME = 'missingadjunct_corpus'
WS = ' '


def get_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")


class Corpus:
    def __init__(self,
                 agent_classes: Tuple[Agent, ...],
                 theme_classes: Tuple[Theme, ...],
                 ) -> None:

        self.agent_classes = agent_classes
        self.theme_classes = theme_classes

        self.logical_forms: List[LogicalForm] = []

        self.date = get_date()

    @property
    def has_forms(self):
        if self.logical_forms:
            return True
        return False

    def populate(self) -> None:
        """create all sentences that are possible given the design"""

        if self.has_forms:
            raise RuntimeError('Corpus already has logical forms. ')

        for theme_class in self.theme_classes:

            for agent_class in self.agent_classes:

                if agent_class.location is not None:
                    if agent_class.location != theme_class.location:
                        continue

                for verb in theme_class.verbs:

                    for agent, theme in product(agent_class.names, theme_class.names):
                        form = LogicalForm(agent=agent,
                                           theme=theme,
                                           verb=verb.name,
                                           instrument=verb.instrument,
                                           location=theme_class.location,
                                           )
                        self.logical_forms.append(form)

    def save(self):

        fn = f'{FILE_NAME}_{self.date}.pkl'
        path_out = (configs.Dirs.pickles / fn)
        with path_out.open('wb') as file:
            pickle.dump(self, file)

        print(f'Saved corpus to {path_out}')

    @classmethod
    def load(cls,
             date: Optional[str] = None,
             ):

        if date is None:
            date = get_date()
        fn = f'{FILE_NAME}_{date}.pkl'

        path_out = (configs.Dirs.pickles / fn)
        with path_out.open('rb') as file:
            res = pickle.load(file)

        return res

    def print_info(self):
        print('Info about corpus:')
        print(f'date={self.date}')

    @lru_cache()
    def is_agent_location_specific(self, agent: str) -> bool:
        for agent_class in self.agent_classes:
            if agent_class.location is not None and agent in agent_class.names:
                return True
        return False

    def gen_logical_forms(self,
                          params: Params,
                          ) -> Generator[LogicalForm, None, None]:
        for epoch in range(params.num_epochs):
            for lf in self.logical_forms:

                if not params.include_location_specific_agents and self.is_agent_location_specific(lf.agent):
                    continue

                if not params.include_location:
                    lf.location = None
                yield lf

    def gen_sentences(self,
                      params: Params,
                      ) -> Generator[str, None, None]:
        for lf in self.gen_logical_forms(params):

            sentence = lf.agent + WS + lf.verb + WS + lf.theme + WS

            if lf.instrument:
                sentence += 'with' + WS + lf.instrument + WS

            if lf.location:
                sentence += 'in' + WS + lf.location + WS

            yield sentence

    def gen_trees(self,
                  params: Params,
                  ) -> Generator[Tuple, None, None]:
        for lf in self.gen_logical_forms(params):
            tree = ()
            yield tree
