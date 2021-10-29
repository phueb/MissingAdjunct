import pickle

from missingadjunct import configs
from missingadjunct.params import Params


fn = 'missingadjunct_corpus_2021-10-29.pkl'
path_out = (configs.Dirs.pickles / fn)
with path_out.open('rb') as file:
    corpus = pickle.load(file)


corpus.print_info()

params = Params(include_location=False,
                include_location_specific_agents=False,
                num_epochs=1
                )

for n, sentence in enumerate(corpus.gen_sentences(params)):

    words = ' '.join([f'{w:<12}' for w in sentence.split()])
    print(f'{n:>6} {words}')
