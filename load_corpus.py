
from missingadjunct.params import Params
from missingadjunct.corpus import Corpus

# parameters that decide how to sample from corpus
params = Params(include_location=False,
                include_location_specific_agents=False,
                num_epochs=1,
                seed=1)

corpus = Corpus.from_params(params)

# print counts of words for all epochs
corpus.print_counts()

# generate sentences for training most models
for n, sentence in enumerate(corpus.get_sentences(params)):
    words = ' '.join([f'{w:<12}' for w in sentence.split()])
    print(f'{n+1:>6} {words}')

# generate trees for training syntax-sensitive models
for n, tree in enumerate(corpus.get_trees(params)):
    print(f'{n+1:>6} {tree}')
