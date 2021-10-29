from typing import Tuple, Generator
import random

from items import Theme, Agent, LogicalForm

TICK = object()


class Design:
    def __init__(self,
                 agents: Tuple[Agent, ...],
                 themes: Tuple[Theme, ...],
                 include_location_specific_agents: bool = False
                 ) -> None:
        self.agents = agents
        self.themes = themes

        if not include_location_specific_agents:
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
                                       location=theme.location,
                                       )
                    yield form
