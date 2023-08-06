Fast Sentence Embeddings (fse)
==================================

Fast Sentence Embeddings is a Python library that serves as an addition to Gensim. This library is intended to compute *summary vectors* for large collections of sentences or documents. 


Features
------------

Find the corresponding blog post here: https://medium.com/@oliverbor/fse-2b1ffa791cf9 

**fse** implements two algorithms for sentence embeddings. You can choose
between *unweighted sentence averages* and *smooth inverse frequency averages*.
In order to use the **fse** model, you first need some pre-trained embedding
gensim embedding model, which is then used by **fse** to compute the sentence embeddings.

After computing sentence embeddings, you can use them in supervised or
unsupervised NLP applications, as they serve as a formidable baseline.

The models here are based on the the smooth inverse frequency embeddings [1]
and the deep-averaging networks [2].

Credit is due to Radim Řehůřek and all contributors for the **awesome** library
and code that gensim provides.


Installation
------------

This software depends on [NumPy, Scipy, Scikit-learn, Gensim, and Wordfreq]. 
You must have them installed prior to installing fse.

As with gensim, it is also recommended you install a fast BLAS library
before installing fse.

The simple way to install **fse** is:

    pip install fse

In case you want to build from the source, just run:

    python setup.py install

Exemplary application
-------------

In order to use **fse** you must first estimate a Gensim model which containes a
gensim.models.keyedvectors.BaseKeyedVectors class, for example 
*Word2Vec* or *Fasttext*. Then you can proceed to compute sentence embeddings
for a corpus.

The current version does not offer multi-core support out of the box.

	from gensim.models import Word2Vec
	sentences = [["cat", "say", "meow"], ["dog", "say", "woof"]]
	model = Word2Vec(sentences, min_count=1)

	from fse.models import Sentence2Vec
	se = Sentence2Vec(model)
	sentences_emb = se.train(sentences)

Sentence Prediction.ipynb contains an example of how to use the library 
with a pre-trained Word2Vec model. compute_sif.py trains a Word2Vec model
on a corpus (i.e, brown) and benchmark_speed.py reproduces the results from
the Medium post.

ToDos
-------------
**[ ]** Various Bugfixes

**[ ]** Feature Testing

**[ ]** Support TaggedLineDocument from Doc2Vec 

**[ ]** Multi Core Implementation

**[ ]** Direct to disc-estimation to to avoid RAM shortage (perhaps?)

**[ ]** Propose as a gensim feature (perhaps?)

Literature
-------------
1. Arora S, Liang Y, Ma T (2017) A Simple but Tough-to-Beat Baseline for Sentence
Embeddings. Int. Conf. Learn. Represent. (Toulon, France), 1–16.

2. Iyyer M, Manjunatha V, Boyd-Graber J, Daumé III H (2015) Deep Unordered 
Composition Rivals Syntactic Methods for Text Classification. Proc. 53rd Annu. 
Meet. Assoc. Comput. Linguist. 7th Int. Jt. Conf. Nat. Lang. Process., 1681–1691.

3. Eneko Agirre, Daniel Cer, Mona Diab, Iñigo Lopez-Gazpio, Lucia Specia. Semeval-2017 Task 1: Semantic Textual Similarity Multilingual and Crosslingual Focused Evaluation. Proceedings of SemEval 2017.

4. Duong, Chi Thang, Remi Lebret, and Karl Aberer. “Multimodal Classification for Analysing Social Media.” The 27th European Conference on Machine Learning and Principles and Practice of Knowledge Discovery in Databases (ECML-PKDD), 2017

Credits
-------------
The STS dataset was released by [3].
The Reddit dataset was released by [4]: https://emoclassifier.github.io 

Copyright
-------------

Author: Oliver Borchers <borchers@bwl.uni-mannheim.de>

Copyright (C) 2019 Oliver Borchers
