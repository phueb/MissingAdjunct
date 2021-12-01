from collections import Counter
import numpy as np
from pyitlib import discrete_random_variable as drv

from missingadjunct.corpus import Corpus


corpus = Corpus(include_location=False,
                include_location_specific_agents=False,
                seed=1,
                num_epochs=1,
                complete_epoch=False,
                )
# get num_templates (this must be computed from a standard non-complete epoch)
lfs_in_epoch = [lf for lf in corpus.get_logical_forms() if lf.epoch == 0]
print(lfs_in_epoch)
num_templates = len(list(lfs_in_epoch))  # should be 64 without a location-specific agents and locations
assert num_templates == 64

# there are 9 possibilities, because there are 3 agents and 3 themes, and they can combine in 9 unique ways
max_h = drv.entropy_pmf([1/9] * 9, base=2)  # this is the entropy that distributions should converge towards

for num_epochs in range(1, 1000):
    corpus = Corpus(include_location=False,
                    include_location_specific_agents=False,
                    seed=1,
                    num_epochs=num_epochs,
                    complete_epoch=False)

    # collect templates (a template is a logical form with a specific verb and instrument, there are 64)
    template2agent_and_theme = {template_id: [] for template_id in range(num_templates)}
    for n, lf in enumerate(corpus.get_logical_forms()):
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