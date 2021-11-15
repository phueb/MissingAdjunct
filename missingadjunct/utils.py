
import pandas as pd
from collections import defaultdict
import numpy as np

from items import theme_classes, experimental_themes

WS = ' '


def make_blank_sr_df():
    """
    Make a blank data frame with phrases in the index and instruments in the columns.

    This dataframe is designed to be filled in with semantic relatedness scores output by distributional semantic models
     trained on the missing-adjunct corpus.
    """

    phrases = []
    instruments = set()
    name2col = defaultdict(list)
    for theme_class in theme_classes[:1]:

        for theme in theme_class.names:

            # collect observed phrases
            for verb in theme_class.verbs:

                if verb.type not in {2, 3}:
                    continue

                phrase_observed = verb.name + WS + theme

                if theme in experimental_themes:
                    theme_type = 'experimental'  # instruments are never observed with this theme
                else:
                    theme_type = 'control'  # instruments are observed with this theme

                # collect
                phrases.append(phrase_observed)
                name2col['verb-type'].append(verb.type)
                name2col['theme-type'].append(theme_type)
                name2col['phrase-type'].append('observed')
                instruments.add(verb.instrument)

            # collect unobserved phrases
            for theme_class_other in theme_classes:

                if theme_class == theme_class_other:
                    continue

                for verb_from_other_theme in theme_class_other.verbs:

                    if verb_from_other_theme.type not in {2, 3}:
                        continue

                    phrase_unobserved = verb_from_other_theme.name + WS + theme

                    # skip cases where verb_from_other_theme is from sister-theme (e.g. "preserve")
                    # because it should be counted once only, with phrase-type=observed
                    if phrase_unobserved in phrases:
                        continue

                    if theme in experimental_themes:
                        theme_type = 'experimental'
                    else:
                        continue

                    # collect
                    phrases.append(phrase_unobserved)
                    name2col['verb-type'].append(verb_from_other_theme.type)
                    name2col['theme-type'].append(theme_type)
                    name2col['phrase-type'].append('unobserved')
                    instruments.add(verb_from_other_theme.instrument)

    # make columns for instruments
    for instrument in sorted(instruments):
        name2col[instrument] = [np.nan] * len(phrases)
    df = pd.DataFrame(data=name2col, index=phrases)
    df.index.name = 'phrase'

    return df


