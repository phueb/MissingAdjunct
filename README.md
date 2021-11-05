
<div align="center">
 <img src="images/logo.png" width="250"> 
</div>

A Python-based tool for generating a corpus of pseudo-English sentences with experimenter-controlled statistics.



## About

This repository generates a corpus for training and evaluating distributional semantic models on a task that requires inferring a missing adjunct (e.g. instrument, location).


## Usage

To use the corpus, see `load_corpus.py`. 


Then, 

```python
for sentence in corpus.get_sentences(params):
    print(sentence)
```


Note: Use a different random seed to produce corpora that differ slightly in their random uniform distributions over agents and themes. 
The purpose of seeds is to enable statistical hypothesis testing.


## Compatibility

Developed on Ubuntu 18.04 and Python 3.7
