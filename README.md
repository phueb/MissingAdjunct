
<div align="center">
 <img src="images/logo.png" width="250"> 
</div>

A Python-based tool for generating a corpus of pseudo-English sentences with experimenter-controlled statistics.



## About

This repository generates a corpus for training and evaluating distributional semantic models on a task that requires inferring a missing adjunct (e.g. instrument, location).


## Usage

First, populate an instance of `Corpus` with logical_forms, and `save()` the populated `Corpus` instance.
The result is a pickle file that can be loaded as shown in `load_corpus.py`.
For example, to exclude instrument adjuncts when training semantic models, use 

```python
params = Params(include_location=False, ...)
```

Then, 

```python
for n, sentence in enumerate(corpus.gen_sentences(params)):
    print(sentence)
```

## Compatibility

Developed on Ubuntu 18.04 and Python 3.7
