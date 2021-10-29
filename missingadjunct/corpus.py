import pickle
from typing import Optional
import datetime

from missingadjunct import configs


FILE_NAME = 'missingadjunct_corpus'


class Corpus:
    def __init__(self):
        self.forms = []

        self.params = {}  # TODO

    def save(self):

        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d")
        fn = f'{FILE_NAME}_{date_string}.pkl'

        path_out = (configs.Dirs.pickles / fn)
        with path_out.open('wb') as file:
            pickle.dump(self, file)

        print(f'Saved corpus to {path_out}')

    @classmethod
    def load(cls,
             date_string: Optional[str] = None,
             ):

        if date_string is None:
            now = datetime.datetime.now()
            date_string = now.strftime("%Y-%m-%d")
        fn = f'{FILE_NAME}_{date_string}.pkl'

        path_out = (configs.Dirs.pickles / fn)
        with path_out.open('rb') as file:
            res = pickle.load(file)

        return res

    def plot_stats(self):
        pass
