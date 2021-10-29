import pickle
from typing import Optional, Generator, List, Tuple
import datetime

from missingadjunct import configs
from items import LogicalForm


FILE_NAME = 'missingadjunct_corpus'
WS = ' '


def get_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")


class Corpus:
    def __init__(self):
        self.forms: List[LogicalForm] = []

        self.params = {}  # TODO

        self.date = get_date()

    def save(self):

        fn = f'{FILE_NAME}_{self.date}.pkl'
        path_out = (configs.Dirs.pickles / fn)
        with path_out.open('wb') as file:
            pickle.dump(self, file)

        print(f'Saved corpus to {path_out}')

    @classmethod
    def load(cls,
             date: Optional[str] = None,
             ):

        if date is None:
            date = get_date()
        fn = f'{FILE_NAME}_{date}.pkl'

        path_out = (configs.Dirs.pickles / fn)
        with path_out.open('rb') as file:
            res = pickle.load(file)

        return res

    def plot_stats(self):
        pass

    def print_info(self):
        print('Info about corpus:')
        print(f'date={self.date}')

    def gen_sentences(self,
                      num_epochs: int = 1,
                      ) -> Generator[str, None, None]:
        for epoch in range(num_epochs):
            for lf in self.forms:

                sentence = lf.agent + WS + lf.verb + WS + lf.theme + WS

                if lf.instrument:
                    sentence += 'with' + WS + lf.instrument + WS

                if lf.location:
                    sentence += 'in' + WS + lf.location + WS

                yield sentence

    def gen_trees(self,
                  num_epochs: int = 1,
                  ) -> Generator[Tuple, None, None]:
        for epoch in range(num_epochs):
            for lf in self.forms:
                tree = ()
                yield tree
