from typing import Optional, Generator, List, Tuple
import random
from functools import lru_cache
from collections import Counter
from itertools import product


from items import LogicalForm
from items import agent_classes, theme_classes, experimental_themes


WS = ' '
WITH = 'with'
IN = 'in'
EOS = '<eos>'


class Corpus:
    def __init__(self,
                 seed: int,
                 include_location: bool,
                 include_location_specific_agents: bool,
                 num_epochs: int,
                 complete_epoch: bool,  # whether to add 1 epoch of all possible combinations in beginning
                 experimental_themes: List[str] = experimental_themes,
                 add_with: bool = True,  # whether to add the preposition "with" before instrument
                 add_in: bool = True,  # whether to add the preposition "in" before location
                 ) -> None:

        self.agent_classes = agent_classes
        self.theme_classes = theme_classes

        self.seed = seed
        self.include_location = include_location
        self.include_location_specific_agents = include_location_specific_agents
        self.include_location_specific_agents = include_location_specific_agents
        self.num_epochs = num_epochs
        self.complete_epoch = complete_epoch
        self.experimental_themes = experimental_themes
        self.add_with = add_with
        self.add_in = add_in

        self.eos = EOS

        self.token2id = {t: n for n, t in enumerate(self.vocab)}

        # check that experimental themes (those which do not occur with instruments) are actually themes in the corpus
        themes = set()
        for theme_class in self.theme_classes:
            themes.update(theme_class.names)
        for theme in self.experimental_themes:
            if theme not in themes:
                raise KeyError(f'{theme} is not a theme in the corpus')

    def get_logical_forms(self) -> Generator[LogicalForm, None, None]:
        """
        for all but first each epoch, get all possible requested forms, and randomly chose from agent and theme.
        in this way, the resulting corpus has a random uniform distribution over agents and themes,
        which enables statistical testing on semantic models without any inherent randomness.
        """

        random.seed(self.seed)

        # first, get all possible requested logical forms once
        for theme_class in self.theme_classes:

            for agent_class in self.agent_classes:

                if agent_class.location is not None:
                    if agent_class.location != theme_class.location:
                        continue

                for verb in theme_class.verbs:

                    for agent, theme in product(agent_class.names, theme_class.names):

                        lf = LogicalForm(agent=agent,
                                         theme=theme,
                                         verb=verb.name,
                                         instrument=verb.instrument,
                                         location=theme_class.location,
                                         epoch=-1,
                                         )

                        # check if lf is requested
                        if not self.include_location_specific_agents and self.is_agent_location_specific(lf.agent):
                            continue
                        if lf.theme in self.experimental_themes:
                            lf.instrument = None
                        if not self.include_location:
                            lf.location = None

                        if self.complete_epoch:
                            yield lf

        # for remaining epochs, sample randomly from agent and theme
        for epoch in range(self.num_epochs):

            for theme_class in self.theme_classes:

                for agent_class in self.agent_classes:

                    if agent_class.location is not None:
                        if agent_class.location != theme_class.location:
                            continue

                    for verb in theme_class.verbs:

                        agent = random.choice(agent_class.names)
                        theme = random.choice(theme_class.names)
                        lf = LogicalForm(agent=agent,
                                         theme=theme,
                                         verb=verb.name,
                                         instrument=verb.instrument,
                                         location=theme_class.location,
                                         epoch=epoch,
                                         )

                        # check if lf is requested
                        if not self.include_location_specific_agents and self.is_agent_location_specific(lf.agent):
                            continue
                        if lf.theme in self.experimental_themes:
                            lf.instrument = None
                        if not self.include_location:
                            lf.location = None

                        yield lf

    @property
    def vocab(self) -> Tuple:

        res = set()
        for lf in self.get_logical_forms():
            res.update([lf.agent, lf.verb, lf.theme, lf.instrument, lf.location])

        res.remove(None)
        if self.add_with:
            res.add(WITH)
        if self.include_location and self.add_in:
            res.add(IN)
        res.add(EOS)

        return tuple(sorted(res))

    def print_counts(self):

        c = Counter()
        for lf in self.get_logical_forms():
            c.update([lf.agent, lf.verb, lf.theme, lf.instrument, lf.location])

        for w, f in c.most_common():
            if w is None:
                continue
            print(f'{w:<12} occurs {f:>6} times')

    @lru_cache()
    def is_agent_location_specific(self, agent: str) -> bool:
        for agent_class in self.agent_classes:
            if agent_class.location is not None and agent in agent_class.names:
                return True

        return False

    def get_sentences(self,
                      include_eos: bool = True,
                      ) -> Generator[str, None, None]:
        for lf in self.get_logical_forms():

            sentence = lf.agent + WS + lf.verb + WS + lf.theme + WS

            if lf.instrument:
                if self.add_with:
                    sentence += WITH + WS + lf.instrument + WS
                else:
                    sentence += lf.instrument + WS

            if lf.location:
                if self.add_in:
                    sentence += IN + WS + lf.location + WS
                else:
                    sentence += lf.location + WS

            if include_eos:
                sentence += WS + EOS

            yield sentence

    def get_trees(self,
                  ) -> Generator[Tuple, None, None]:

        for lf in self.get_logical_forms():

            # location is included
            if self.include_location:

                # instrument is included
                if lf.instrument:
                    if self.add_with and self.add_in:
                        tree = (lf.agent, (((lf.verb, lf.theme), (WITH, lf.instrument)), (IN, lf.location)))
                    elif self.add_with and not self.add_in:
                        tree = (lf.agent, (((lf.verb, lf.theme), (WITH, lf.instrument)), lf.location))
                    else:
                        tree = (lf.agent, (((lf.verb, lf.theme), lf.instrument), lf.location))

                # instrument is not included
                else:
                    if self.add_in:
                        tree = (lf.agent, ((lf.verb, lf.theme), (IN, lf.location)))
                    else:
                        tree = (lf.agent, ((lf.verb, lf.theme), lf.location))

            # location is not included
            else:

                # instrument is included
                if lf.instrument:
                    if self.add_with:
                        tree = (lf.agent, ((lf.verb, lf.theme), (WITH, lf.instrument)))
                    else:
                        tree = (lf.agent, ((lf.verb, lf.theme), lf.instrument))

                # instrument is not included
                else:
                    tree = (lf.agent, (lf.verb, lf.theme))

            yield tree
