from missingadjunct.corpus import Corpus


corpus = Corpus.load()

corpus.print_info()

for sentence in corpus.gen_sentences():

    words = [f'{w:<12}' for w in sentence.split()]
    print(' '.join(words))
