# keyword_ranker

The Keyword Ranker uses the Rapid Automatic Keyword Extraction algorithm (RAKE) to extract the most relevant keywords from a reference corpus, checks them against other documents and ranks them depending on to which degree those keywords are represented in the aformentioned documents.

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

## Usage

```python
from keyword_ranker import KeywordRanker

kr = KeywordRanker()

# Uses english stopwords from the smartstoplist.txt included in the package by default.
# You can specify your own set of stopwords by adding the filepath as an argument.


kr.fit() # Extracts and scores the keywords from the corpus.

kr.rank() # Ranks the corpus keywords with regards to the provided documents.
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
