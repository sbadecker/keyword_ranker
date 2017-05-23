import os
from unittest import TestCase
from keyword_ranker.kwr import KeywordRanker

test_text = os.path.dirname(__file__)+'/test_text.txt'

class TestRank(TestCase):
    def self_rank(self):
        kr = KeywordRanker()
        kr.fit(test_text)
        kwr, kwd = kr.rank(2, test_text)
        self.assertequal(kr.corpus_keywords, kwr)
