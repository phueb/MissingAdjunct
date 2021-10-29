

from missingadjunct.corpus import Corpus

from items import agent_classes, theme_classes


def main():
    """
    populate corpus with all possible sentences.
    the corpus object is save to disk and can be used to selectively exclude sentences.
    """

    corpus = Corpus(agent_classes=agent_classes, theme_classes=theme_classes)
    corpus.populate()
    corpus.save()


if __name__ == '__main__':

    main()

