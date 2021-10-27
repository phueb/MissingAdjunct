from typing import Tuple, Generator
import random

from missingadjunct import configs
from items import Theme, Agent, LogicalForm, Verb

TICK = object()


class Design:
    def __init__(self,
                 agents: Tuple[Agent, ...],
                 themes: Tuple[Theme, ...],
                 ) -> None:
        self.agents = agents
        self.themes = themes

        if not configs.Corpus.include_location_specific_agents:
            self.agents = [a for a in self.agents if a.location is None]

    def epoch(self) -> Generator[LogicalForm, None, None]:

        for theme in self.themes:

            for agent in self.agents:

                if agent.location is not None:
                    if agent.location != theme.location:
                        continue

                for verb in theme.verbs:

                    form = LogicalForm(agent=random.choice(agent.names),
                                       theme=random.choice(theme.names),
                                       verb=verb.name,
                                       instrument=verb.instrument,
                                       location=theme.location if configs.Corpus.include_location else None,
                                       )
                    yield form
