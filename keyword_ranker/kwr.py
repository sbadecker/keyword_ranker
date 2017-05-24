'''
The Keyword Ranker uses the Rapid Automatic Keyword Extraction algorithm (RAKE)
to extract the most relevant keywords from a reference corpus, and ranks them
depending on the degree to which they are represented in other benchmark
documents.

For more infos and examples visit:
https://github.com/sbadecker/keyword_ranker

'''

import os
from keyword_ranker import rake
from collections import defaultdict


smartstoplist = os.path.dirname(__file__)+'/smartstoplist.txt'


def txt_reader(file_txt, encoding='utf-8'):
    f = open(file_txt, 'r', encoding=encoding)
    text = f.read()
    return text


class KeywordRanker(object):
    '''Generates a KeywordRanker object.

    Parameters
    ----------
    min_char_length : int
        The minimum number of characters a word must have to be included.
    max_words_length : int
        The Maximum number of words a keyword can have to be included.
    min_keyword_frequency : int
        Minimum number of occurances a keyword must have in the  corpus to be
        included.
    lemmatize : bool
        Use lemmatization (NLTKs WordNetLemmatizer).
    stopwords_path : str
        Path and filename of a file containing stop words. Each stopword needs
        to be on a new line.


    Attributes
    ----------
    corpus_keywords : int
        Includes the keywords and corresponding scores.


    Returns
    ------
    out : KeywordRanker object


    Notes
    -----
    Using large values for min_keyword_frequency and min_char_length will result
    in no keywords being found and will raise an error when fitting the corpus.

    '''
    def __init__(self, min_char_length=1, max_words_length=3,
                min_keyword_frequency=3, lemmatize=True,
                stopwords_path=smartstoplist):
        self.min_char_length = min_char_length
        self.max_words_length = max_words_length
        self.min_keyword_frequency = min_keyword_frequency
        self.corpus_keywords = None
        self.lemmatize = lemmatize
        self.stopwords_path = stopwords_path
        self.stopwords_pattern = rake.build_stopword_regex(self.stopwords_path)

    def fit(self, corpus_txt, encoding='utf-8'):
        '''
        Extracts and scores the keywords of the provided corpus and stores
        them in self.corpus_keywords.

        Parameters
        ----------
        corpus_txt : str
            Path and filename of corpus document.
        encoding : str
            Specifies type of encoding.


        Notes
        -----
        Using large values for min_keyword_frequency and min_char_length will result
        in no keywords being found and will raise an error when fitting the corpus.

        '''
        rake_object = rake.Rake(self.stopwords_path, self.min_char_length,
                        self.max_words_length, self.min_keyword_frequency,
                        self.lemmatize)
        text = txt_reader(corpus_txt, encoding=encoding)
        self.corpus_keywords = rake_object.run(text)
        if self.corpus_keywords == []:
            raise ValueError('No keywords for these input parameters.')


    def wordscores(self, transcript_txt, encoding='utf-8'):
        text = txt_reader(transcript_txt, encoding=encoding)
        sentencelist = rake.split_sentences(text)
        phraselist = rake.generate_candidate_keywords(sentencelist,
                        self.stopwords_pattern, self.min_char_length,
                        self.max_words_length, self.lemmatize)
        wordscores = rake.calculate_word_scores(phraselist)
        return wordscores

    def rank(self, n, *transcripts, absolute_deviation=False, encoding='utf-8'):
        '''
        Calls the wordscores function to generate a wordscores dictionary for
        the provided transcripts and scores the top n corpus keywords on this
        dictionary.

        Parameters
        ----------
        n : int
            Number of corpus keywords to analyze. Picks the highest scoring
            corpus keywords first.
        *transcrips : str
            Paths and filenames to arbitrary number of transcripts that the
            corpus keywords should be scored against.
        absolute_deviation : bool
            Calculate absolute deviation of keyword score from corpus to
            documents. If set to False, relative deviation will be calculated.
        encoding : str
            Specifies type of encoding.


        Returns
        ------
        keyword_rank : list of tuples
            Includes the keywords and corresponding scores on the transcripts.
        keyword_deviation : list of tuples
            Includes the keywords and corresponding deviation from their scores
            on the corpus.

        '''
        top_n_corpus = [word[0] for word in self.corpus_keywords[:n]]
        keyword_scores = defaultdict(int)
        n_transcripts = len(transcripts)
        for transcript in transcripts:
            wordscores = self.wordscores(transcript, encoding=encoding)
            for keyword in top_n_corpus:
                keyword_score = 0
                for word in keyword.split(' '):
                    try:
                        keyword_score += wordscores[word]/n_transcripts
                    except KeyError:
                        pass
                keyword_scores[keyword] += keyword_score
        keyword_rank = [(key, keyword_scores[key]) for key in
                        sorted(keyword_scores, key=keyword_scores.get,
                        reverse=True)]
        keyword_deviation = self.get_deviation(keyword_rank, n,
                            absolute_deviation)
        return keyword_rank, keyword_deviation

    def get_deviation(self, keyword_rank, n, absolute_deviation):
        if n > len(self.corpus_keywords):
            raise ValueError('n too large. Pick n of max. {}.' \
            .format(len(self.corpus_keywords)))
        kwr_sorted = sorted(keyword_rank)
        ckw_sorted = sorted(self.corpus_keywords[:n])
        if absolute_deviation:
            keyword_deviation = [(kwr_sorted[i][0], (kwr_sorted[i][1]
                                - ckw_sorted[i][1])) for i in range(n)]
        else:
            keyword_deviation = [(kwr_sorted[i][0], (kwr_sorted[i][1]
                                - ckw_sorted[i][1]) / ckw_sorted[i][1]) for i in
                                range(n)]
        kw_zipped = zip(keyword_deviation, kwr_sorted)
        kw_zipped_sorted = sorted(kw_zipped, key=lambda x: -x[1][1])
        keyword_deviation = [kw[0] for kw in kw_zipped_sorted]
        return keyword_deviation
