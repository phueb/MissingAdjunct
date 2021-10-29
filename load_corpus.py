import pickle

from missingadjunct.params import Params


with open('missingadjunct_corpus_2021-10-29.pkl', 'rb') as file:
    corpus = pickle.load(file)

# print counts of words for 1 epoch only
corpus.print_counts()

# parameters that decide how to sample from corpus
params = Params(include_location=False,
                include_location_specific_agents=False,
                num_epochs=1,
                instrument_silent_themes=['pepper',
                                          'orange',
                                          'blender',
                                          'bowl',
                                          'tomato-juice',
                                          'cookie',
                                          'turkey',
                                          'tilapia',
                                          'sock',
                                          'ash',
                                          'faceshield',
                                          'workstation',
                                          'brake-fluid',
                                          'motorcycle',
                                          'marble',
                                          'copper',
                                          ],
                )

# generate sentences for training most models
for n, sentence in enumerate(corpus.gen_sentences(params)):
    words = ' '.join([f'{w:<12}' for w in sentence.split()])
    print(f'{n:>6} {words}')

# generate trees for training syntax-sensitive models
for n, tree in enumerate(corpus.gen_trees(params)):

    print(f'{n:>6} {tree}')
