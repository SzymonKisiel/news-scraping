import json
from typing import List
from models.search_term import SearchTerm
from models.article import Article
from models.client import Client


class Sentiment:
    id: int

    article_id: int
    article: Article

    search_term_id: int
    search_term: SearchTerm

    sentence: str
    positive_score: float
    neutral_score: float
    negative_score: float
    overall_sentiment: int

    def __init__(self,
                 id: int = 0,
                 article_id: int = 0,
                 search_term_id: int = 0,
                 article: Article = None,
                 search_term: SearchTerm = None,
                 sentence: str = '',
                 positive_score: float = 0.,
                 neutral_score: float = 0.,
                 negative_score: float = 0.,
                 overall_sentiment: int = 0):
        self.id = id
        self.article_id = article_id
        self.article = article
        self.search_term_id = search_term_id
        self.search_term = search_term
        self.sentence = sentence
        self.positive_score = positive_score
        self.neutral_score = neutral_score
        self.negative_score = negative_score
        self.overall_sentiment = overall_sentiment

    def to_dict(self):
        return {
            'id': self.id,
            'article_id': self.article_id,
            'article': self.article.to_dict(),
            'search_term_id': self.search_term_id,
            'search_term': self.search_term.to_dict(),
            'sentence': self.sentence,
            'positive_score': self.positive_score,
            'neutral_score': self.neutral_score,
            'negative_score': self.negative_score,
            'overall_sentiment': self.overall_sentiment
        }
