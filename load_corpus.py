
from missingadjunct.corpus import Corpus


corpus = Corpus(include_location=True,
                include_location_specific_agents=False,
                seed=1,
                num_epochs=1,
                complete_epoch=True,
                add_with=True,
                add_in=False,
                strict_compositional=True,  # todo test
                )

# print counts of words for all epochs
corpus.print_counts()

# generate sentences for training most models
for n, sentence in enumerate(corpus.get_sentences()):
    words = ' '.join([f'{w:<12}' for w in sentence.split()])
    print(f'{n+1:>6} {words}')

# generate trees for training syntax-sensitive models
for n, tree in enumerate(corpus.get_trees()):
    print(f'{n+1:>6} {tree}')
