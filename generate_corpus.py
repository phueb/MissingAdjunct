from typing import Coroutine, Generator, Union, Dict
import colorlog

from missingadjunct import configs
from missingadjunct.corpus import Corpus
from missingadjunct.design import Design

from items import agents, themes


handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    fmt='%(log_color)s%(levelname)s:%(name)s:%(message)s',
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'blue',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
))

log_language = colorlog.getLogger('language')
log_language.addHandler(handler)
log_language.setLevel('DEBUG')


def modify_state(
                 ) -> Coroutine[None, None, None]:

    yield None


def main():

    design = Design(agents=agents, themes=themes)
    corpus = Corpus()

    for i in range(configs.Corpus.num_epochs):

        for form in design.epoch():
            corpus.forms.append(form)
            log_language.info(form)

        corpus.plot_stats()  # keep track of convergence

    corpus.save()


if __name__ == '__main__':

    main()
