# keyword_ranker

The Keyword Ranker uses the Rapid Automatic Keyword Extraction algorithm
(RAKE) to extract the most relevant keywords from a reference corpus,
and ranks them depending on the degree to which they are represented in other
benchmark documents.

## Setup

### Using pip

```bash
pip install keyword_ranker
```

### Directly from the repository

```bash
git clone hhttps://github.com/sbadecker/keyword_ranker.git
python keyword_ranker/setup.py install
```

## Dependencies

This package requires the modules NLTK and six and will install them if necessary.
To use lemmatization, nltk.corpus.wordnet is required an will be downloaded if necessary.

## Languages

This package comes with an English stopwords list. You can specify your own set of stopwords by adding the filepath as an argument (stopwords_path).
As of now, lemmatization is only supported in for English documents.

## Usage

```python
from keyword_ranker.kwr import KeywordRanker

kr = KeywordRanker()

kr.fit() # Extracts and scores the keywords from the corpus.
# example: kr.fit(corpus.txt)

kr.rank() # Ranks the n highest scoring corpus keywords with regards to the provided documents.
# example: kr.rank(10, document1.txt, document2.txt)

# Tests can be run in the package directory using nosetests.
```

## References

This package uses a Python implementation of the RAKE algorithm as mentiones in paper [Automatic keyword extraction from individual documents by Stuart Rose, Dave Engel, Nick Cramer and Wendy Cowley](https://www.researchgate.net/profile/Stuart_Rose/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents/links/55071c570cf27e990e04c8bb.pdf).
The original code included in rake.py can be found here: https://github.com/zelandiya/RAKE-tutorial. It has been extended by me to support lemmatization using WordNetLemmatizer from the NLTK.

## Versions of python this code is tested against

- 3.6

## Contributing

### Bug Reports and Feature Requests
Please use [issue tracker](https://github.com/sbadecker/keyword_ranker/issues) for reporting bugs or feature requests.


### Development
Pull requests are most welcome.
