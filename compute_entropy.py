from collections import Counter
import pickle
from pathlib import Path
import numpy as np
from pyitlib import discrete_random_variable as drv

from missingadjunct.params import Params


CORPUS_NAME = 'missingadjunct_corpus_2021-11-03'
SEED = 0

MAX_NUM_EPOCHS = 1000

path_corpus_file = (Path(CORPUS_NAME) / f'{CORPUS_NAME}_{SEED}.pkl')
with path_corpus_file.open('rb') as file:
    corpus = pickle.load(file)

params = Params(include_location=False,
                include_location_specific_agents=False,
                num_epochs=1,
                instrument_silent_themes=[],
                )

lfs_in_epoch = [lf for lf in corpus.get_logical_forms(params) if lf.epoch == 0]
num_templates = len(list(lfs_in_epoch))  # should be 64 without a location-specific agents and locations
print(num_templates)

# there are 9 possibilities, because there are 3 agents and 3 themes, and they can combine in 9 unique ways
max_h = drv.entropy_pmf([1/9] * 9, base=2)  # this is the entropy that distributions should converge towards

for num_epochs in range(1, MAX_NUM_EPOCHS):
    # parameters that decide how to sample from corpus
    params = Params(include_location=False,
                    include_location_specific_agents=False,
                    num_epochs=num_epochs,
                    instrument_silent_themes=[],
                    )

    # collect templates (a template is a logical form with a specific verb and instrument, there are 64)
    template2agent_and_theme = {template_id: [] for template_id in range(num_templates)}
    for n, lf in enumerate(corpus.get_logical_forms(params)):
        if lf.epoch == -1:
            continue
        template_id = n % num_templates
        template2agent_and_theme[template_id].append((lf.agent, lf.theme))

    # compute entropy for each agent-theme distribution (one per template)
    hs = []
    for template, agent_and_theme in template2agent_and_theme.items():
        c = Counter(agent_and_theme)
        f_obs = [f for f in c.values()] + [0] * (9 - len(c))
        h = drv.entropy(f_obs)
        hs.append(h)

    print(f'After {num_epochs:>3} epochs | Average entropy = {np.mean(hs).round(3)} Max entropy = {max_h.round(3)}')