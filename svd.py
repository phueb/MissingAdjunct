import numpy as np
from itertools import product

from missingadjunct.params import Params
from missingadjunct.corpus import Corpus


# parameters that decide how to sample from corpus
params = Params(include_location=False,
                include_location_specific_agents=False,
                num_epochs=1,
                seed=1)

corpus = Corpus.from_params(params)

# collect co-occurrences from epoch -1
num_vocab = len(corpus.vocab)
co_mat = np.zeros((num_vocab, num_vocab))
for lf in corpus.logical_forms:

    if lf.epoch != -1:
        continue

    if not params.include_location_specific_agents and corpus.is_agent_location_specific(lf.agent):
        continue

    if lf.theme in params.experimental_themes:
        lf.instrument = None

    if not params.include_location:
        lf.location = None

    items = [lf.agent, lf.verb, lf.theme, lf.instrument]
    for a, b in product(items, items):
        if a == b:
            continue
        if a is None or b is None:
            continue

        print(a, b)

print(corpus.vocab)
# a, s, v = np.linalg.svd(a, full_matrices=False, compute_uv=True)

