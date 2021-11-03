import pickle
from pathlib import Path

from missingadjunct.params import Params


CORPUS_NAME = 'missingadjunct_corpus_2021-11-02'
SEED = 1

path_corpus_file = (Path(CORPUS_NAME) / f'{CORPUS_NAME}_{SEED}.pkl')
with path_corpus_file.open('rb') as file:
    corpus = pickle.load(file)

# print counts of words for all epochs
corpus.print_counts()

# parameters that decide how to sample from corpus
params = Params(include_location=False,
                include_location_specific_agents=False,
                num_epochs=3,  # this number selects how many of the 1000 existing epochs should be retrieved
                )

# generate sentences for training most models
for n, sentence in enumerate(corpus.get_sentences(params)):
    words = ' '.join([f'{w:<12}' for w in sentence.split()])
    print(f'{n+1:>6} {words}')

# generate trees for training syntax-sensitive models
for n, tree in enumerate(corpus.get_trees(params)):
    print(f'{n+1:>6} {tree}')
