
<div align="center">
 <img src="images/logo.png" width="250"> 
</div>

A Python-based tool for generating a corpus of pseudo-English sentences with experimenter-controlled statistics.



## About

This repository generates a corpus for training and evaluating distributional semantic models on a task that requires inferring a missing adjunct (e.g. instrument, location).


## Usage

To use the corpus, see `load_corpus.py`. 
This script loads a pickle file, included in this repository, and is ready for training semantic models.
For example, to exclude instrument adjuncts when training semantic models, use 

```python
params = Params(include_location=False, ...)
```

Note: You will have to copy `params.py` or its contents to your own project.

Then, 

```python
for sentence in corpus.get_sentences(params):
    print(sentence)
```

Note: There are multiple files saved in the same corpus location. 
These files correspond to different random seeds, and produce corpora that differ slightly in their random uniform distributions over agents and themes. 
The purpose of seeds is to enable statistical hypothesis testing.

## Advanced

To generate a pickled `Corpus` instance:
1. populate an instance of `Corpus` with `logical_forms`
2. `save()` the populated `Corpus` instance.

The result is a pickle file that can be loaded as shown in `load_corpus.py`.

## Compatibility

Developed on Ubuntu 18.04 and Python 3.7
