from typing import Optional, Generator, List, Tuple
import datetime
import random
from functools import lru_cache
from collections import Counter
from itertools import product


from items import LogicalForm
from items import agent_classes, theme_classes, experimental_themes


FILE_NAME = 'missingadjunct_corpus'
WS = ' '


class Corpus:
    def __init__(self,
                 seed: int,
                 include_location: bool,
                 include_location_specific_agents: bool,
                 experimental_themes: List[str] = experimental_themes,
                 ) -> None:

        self.agent_classes = agent_classes
        self.theme_classes = theme_classes

        self.seed = seed
        self.include_location = include_location
        self.include_location_specific_agents = include_location_specific_agents
        self.include_location_specific_agents = include_location_specific_agents
        self.experimental_themes = experimental_themes

        self.max_num_epochs = 1000  # max num epoch - corpus has statistically converged by then

        self.logical_forms: List[LogicalForm] = []
        self.populate()

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

        # first, populate with all possible logical forms once
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
                                           epoch=-1,
                                           )
                        self.logical_forms.append(form)

        # for remaining epochs, sample randomly from agent and theme
        for epoch in range(self.max_num_epochs):

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

    @property
    def vocab(self) -> Tuple[str]:
        assert self.has_forms

        res = set()
        for lf in self.logical_forms:
            res.update([lf.agent, lf.verb, lf.theme, lf.instrument, lf.location])

        res.remove(None)

        return tuple(sorted(res))

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
                          num_epochs: int,
                          ) -> Generator[LogicalForm, None, None]:

        assert self.has_forms

        if num_epochs > self.max_num_epochs:
            raise AttributeError(f'Requested {num_epochs} epochs but corpus was populated with {self.max_num_epochs} epochs')

        # check that silent-instrument themes are actually themes in the corpus
        themes = set()
        for theme_class in self.theme_classes:
            themes.update(theme_class.names)
        for theme in self.experimental_themes:
            if theme not in themes:
                raise KeyError(f'{theme} is not a theme in the corpus')

        for lf in self.logical_forms:

            if not lf.epoch < num_epochs:
                continue

            if not self.include_location_specific_agents and self.is_agent_location_specific(lf.agent):
                continue

            if lf.theme in self.experimental_themes:
                lf.instrument = None

            if not self.include_location:
                lf.location = None
            yield lf

    def get_sentences(self,
                      num_epochs: int,
                      ) -> Generator[str, None, None]:
        for lf in self.get_logical_forms(num_epochs):

            sentence = lf.agent + WS + lf.verb + WS + lf.theme + WS

            if lf.instrument:
                sentence += 'with' + WS + lf.instrument + WS

            if lf.location:
                sentence += 'in' + WS + lf.location + WS

            yield sentence

    def get_trees(self,
                  num_epochs: int,
                  ) -> Generator[Tuple, None, None]:
        for lf in self.get_logical_forms(num_epochs):
            if self.include_location:
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
