

from missingadjunct.corpus import Corpus

from items import agent_classes, theme_classes


NUM_EPOCHS = 100
NUM_SEEDS = 10


def main():
    """
    populate corpus with all possible sentences.
    the corpus object is save to disk and can be used to selectively exclude sentences.
    """

    for seed in range(NUM_SEEDS):
        corpus = Corpus(agent_classes=agent_classes,
                        theme_classes=theme_classes,
                        seed=seed,
                        num_epochs=NUM_EPOCHS,
                        )
        corpus.populate()
        corpus.save()


if __name__ == '__main__':

    main()

