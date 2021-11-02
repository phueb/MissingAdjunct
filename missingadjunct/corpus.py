import pickle
from typing import Optional, Generator, List, Tuple
import datetime
import random
from functools import lru_cache
from collections import Counter

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
                 seed: int,
                 num_epochs: int,
                 ) -> None:

        self.agent_classes = agent_classes
        self.theme_classes = theme_classes
        self.seed = seed
        self.num_epochs = num_epochs

        self.logical_forms: List[LogicalForm] = []

        self.date = get_date()

    @property
    def has_forms(self):
        if self.logical_forms:
            return True
        return False

    def populate(self) -> None:
        """
        for each epoch, get all possible templates, and randomly chose from agent and theme.
        in this way, the resulting corpus has a random uniform distribution over agents and themes,
        which enables statistical testing on semantic models without any inherent randomness.
        """

        random.seed(self.seed)

        if self.has_forms:
            raise RuntimeError('Corpus already has logical forms. ')

        for epoch in range(self.num_epochs):

            for theme_class in self.theme_classes:

                for agent_class in self.agent_classes:

                    if agent_class.location is not None:
                        if agent_class.location != theme_class.location:
                            continue

                    for verb in theme_class.verbs:

                        agent = random.choice(agent_class.names)
                        theme = random.choice(theme_class.names)
                        form = LogicalForm(agent=agent,
                                           theme=theme,
                                           verb=verb.name,
                                           instrument=verb.instrument,
                                           location=theme_class.location,
                                           epoch=epoch,
                                           )
                        self.logical_forms.append(form)

    def save(self):

        fn = f'{FILE_NAME}_{self.date}_{self.seed}.pkl'
        path_out = (configs.Dirs.root / f'{FILE_NAME}_{self.date}' / fn)
        if not path_out.parent.exists():
            path_out.parent.mkdir()
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

        path_out = (configs.Dirs.root / fn)
        with path_out.open('rb') as file:
            res = pickle.load(file)

        res.check_integrity()

        return res

    def print_counts(self):
        assert self.has_forms

        c = Counter()
        for lf in self.logical_forms:
            c.update([lf.agent, lf.verb, lf.theme, lf.instrument, lf.location])

        for w, f in c.most_common():
            if w is None:
                continue
            print(f'{w:<12} occurs {f:>6} times')

    def check_integrity(self):
        assert self.has_forms
        assert len(set(self.logical_forms)) == len(self.logical_forms)

    @lru_cache()
    def is_agent_location_specific(self, agent: str) -> bool:
        for agent_class in self.agent_classes:
            if agent_class.location is not None and agent in agent_class.names:
                return True

        return False

    def get_logical_forms(self,
                          params: Params,
                          ) -> Generator[LogicalForm, None, None]:

        if params.num_epochs > self.num_epochs:
            raise AttributeError(f'Requested {params.num_epochs} epochs but corpus was populated with {self.num_epochs} epochs')

        # check that silent-instrument themes are actually themes in the corpus
        themes = set()
        for theme_class in self.theme_classes:
            themes.update(theme_class.names)
        for theme in params.instrument_silent_themes:
            if theme not in themes:
                raise KeyError(f'{theme} is not a theme in the corpus')

        for lf in self.logical_forms:

            if not lf.epoch < params.num_epochs:
                continue

            if not params.include_location_specific_agents and self.is_agent_location_specific(lf.agent):
                continue

            if lf.theme in params.instrument_silent_themes:
                lf.instrument = None

            if not params.include_location:
                lf.location = None
            yield lf

    def get_sentences(self,
                      params: Params,
                      ) -> Generator[str, None, None]:
        for lf in self.get_logical_forms(params):

            sentence = lf.agent + WS + lf.verb + WS + lf.theme + WS

            if lf.instrument:
                sentence += 'with' + WS + lf.instrument + WS

            if lf.location:
                sentence += 'in' + WS + lf.location + WS

            yield sentence

    def get_trees(self,
                  params: Params,
                  ) -> Generator[Tuple, None, None]:
        for lf in self.get_logical_forms(params):
            if params.include_location:
                if lf.instrument:
                    tree = (lf.agent, (((lf.verb, lf.theme), lf.instrument), lf.location))
                else:
                    tree = (lf.agent, ((lf.verb, lf.theme), lf.instrument))
            else:
                if lf.instrument:
                    tree = (lf.agent, ((lf.verb, lf.theme), lf.instrument))
                else:
                    tree = (lf.agent, (lf.verb, lf.theme))
            yield tree
