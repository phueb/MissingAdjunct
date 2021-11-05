"""
Train a HAL-like model on epoch -1 which contains the full design without randomness.

Then show that the vector "preserve pepper" (composed using addition) are equally similar to "vinegar" and "dehydrator".
This is expected given our design.

Then show that the problem can be solved
if reducing the dimensionality of vectors with SVD to a specific number of dimensions.
but, crucially, only a specific number of singular dimensions can solve the problem.
ultimately, then, the problem can be reduced toa feature-selection problem
(e.g choosing the number of reduced dimensions).
"""
import numpy as np
from itertools import product
from sklearn.metrics.pairwise import cosine_similarity
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
w2id = {w: n for n, w in enumerate(corpus.vocab)}
co_mat = np.zeros((num_vocab, num_vocab), dtype=int)
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

        a_id = w2id[a]
        b_id = w2id[b]
        co_mat[a_id, b_id] += 1


# show that similarity between "preserve pepper" is identical to "vinegar" and "dehydrator"
v1 = co_mat[w2id['preserve']]
v2 = co_mat[w2id['pepper']]
vt = co_mat[w2id['vinegar']]
vd = co_mat[w2id['dehydrator']]
v3 = v1 + v2
# print(cosine_similarity(v3, vt))
# print(cosine_similarity(v3, vd))

u, s, v = np.linalg.svd(co_mat, full_matrices=False, compute_uv=True)
for num_d in range(2, co_mat.shape[1]):
    u_ = u[:, :num_d]
    v1 = u_[w2id['preserve']]
    v2 = u_[w2id['pepper']]
    vt = u_[w2id['vinegar']]
    vd = u_[w2id['dehydrator']]
    v3 = v1 + v2
    sim_t = cosine_similarity(v3[np.newaxis, :], vt[np.newaxis, :]).round(4).item()
    sim_d = cosine_similarity(v3[np.newaxis, :], vd[np.newaxis, :]).round(4).item()
    print(sim_t, sim_d)
    if sim_t > sim_d:
        print('HIT')
    else:
        print('MISS')



