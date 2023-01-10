import logging

from typing import List
from datetime import datetime
from database.database import get_mysql_db_connection
from database.repositories.article_repository import ArticleRepository
from database.repositories.client_repository import ClientRepository
from database.repositories.search_term_repository import SearchTermRepository
from database.repositories.sentiment_repository import SentimentRepository
from models.article import Article
from models.search_term import SearchTerm
from models.sentiment import Sentiment
from models.sentiment_score import SentimentScore
from services.models import UpdateSentimentRequest
from services.sentiment_analyse_service import SentimentAnalyseService


class SentimentService:
    logger: logging.Logger
    article_repository: ArticleRepository
    client_repository: ClientRepository
    search_term_repository: SearchTermRepository
    sentiment_repository: SentimentRepository

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.article_repository = ArticleRepository(logger)
        self.client_repository = ClientRepository(logger)
        self.search_term_repository = SearchTermRepository(logger)
        self.sentiment_repository = SentimentRepository(logger)
        # self.sentiment_analyser = SentimentAnalyser()
        self.sentiment_analyse_service = SentimentAnalyseService(logger)

    def get_all_by_search_term(self, search_term: str):
        return self.sentiment_repository.get_all_by_search_term_name(search_term)

    def get_all_by_search_term_id(self, search_term_id: int):
        return self.sentiment_repository.get_all_by_search_term_id(search_term_id)

    # def test(self):
    #     # print('START MEGA TEST')
    #     # self.update()
    #     # print('STOP MEGA TEST')
    #     print('START SENTENCE TEST')
    #     sentences = self.__split_to_sentences("Zdanie.     Teraz.", "McDonalds jest dziwne", "Test")
    #     for sentence in sentences:
    #         print(sentence)
    #     print('END SENTENCE TEST')
    #     #
    #     # print('START SENTIMENT TEST')
    #     # for sentence in sentences:
    #     #     print(sentence)
    #     #     # score = self.sentiment_analyser.analyse(sentence)
    #     #     score = self.sentiment_analyse_service.analyse(sentence)
    #     #     print({
    #     #         "neg": score.negative_score,
    #     #         "neu": score.neutral_score,
    #     #         "pos": score.positive_score
    #     #     })
    #     # print('END SENTIMENT TEST')
