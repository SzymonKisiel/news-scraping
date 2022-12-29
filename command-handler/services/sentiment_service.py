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
from utils.sentencizer import Sentencizer


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
        self.sentencizer = Sentencizer()
        # self.sentiment_analyser = SentimentAnalyser()
        self.sentiment_analyse_service = SentimentAnalyseService(logger)

    def __split_to_sentences(self, *texts) -> List[str]:
        text = ' '.join(texts)
        return self.sentencizer.sentecize(text)

    def __get_last_created_at(self, articles: List[Article]) -> datetime:
        if not articles:
            return datetime.min
        last_created_at = articles[0].created_at

        for article in articles:
            created_at = article.created_at
            if created_at > last_created_at:
                last_created_at = created_at

        return last_created_at

    def get_all_by_search_term(self, search_term: str):
        pass

    def __update_sentiments_for_term(self, term: SearchTerm):
        # Init connection
        cnx = get_mysql_db_connection()

        # find all articles which contain word AND do not have sentiment calculated
        articles = self.article_repository.search_created_after(
            term.search_term,
            term.updated_sentiments_at,
            connection=cnx)
        if not articles:
            return
        last_created_at = self.__get_last_created_at(articles)
        for article in articles:
            # split article to sentences
            sentences = self.__split_to_sentences(article.title, article.subtitle, article.text)

            # remove sentences without search term
            # TODO

            # calculate sentiment for each sentence
            for sentence in sentences:
                sentiment_score = self.sentiment_analyse_service.analyse(sentence)
                sentiment = Sentiment(
                    article_id=article.article_id,
                    search_term_id=term.id,
                    sentence=sentence,
                    negative_score=sentiment_score.negative_score,
                    neutral_score=sentiment_score.neutral_score,
                    positive_score=sentiment_score.positive_score,
                    overall_sentiment=sentiment_score.to_overall_sentiment_id()
                )
                self.sentiment_repository.insert_sentiment(sentiment, connection=cnx)

        self.search_term_repository.set_term_updated_sentiments_at(term.id, last_created_at, connection=cnx)

        # Commit and close the connection
        cnx.commit()
        cnx.close()

    def update(self, request: UpdateSentimentRequest):
        term = self.search_term_repository.get_by_search_term_name(request.search_term)
        self.__update_sentiments_for_term(term)

    def update_all(self):
        terms = self.search_term_repository.get_all_search_terms()
        for term in terms:
            self.__update_sentiments_for_term(term)

    def test(self):
        print('START MEGA TEST')
        # self.update()
        print('STOP MEGA TEST')
        # print('START SENTENCE TEST')
        # sentences = self.__split_to_sentences("Hejka. Chciałbym się dowiedzieć kiedy prof. Stanisław będzie dostępny, kiedy można się z nim kontaktować lub cokolwiek. Proszę, powiedz mi.     Teraz.", "McDonalds jest dziwne.")
        # for sentence in sentences:
        #     print(sentence)
        # print('END SENTENCE TEST')
        #
        # print('START SENTIMENT TEST')
        # for sentence in sentences:
        #     print(sentence)
        #     # score = self.sentiment_analyser.analyse(sentence)
        #     score = self.sentiment_analyse_service.analyse(sentence)
        #     print({
        #         "neg": score.negative_score,
        #         "neu": score.neutral_score,
        #         "pos": score.positive_score
        #     })
        # print('END SENTIMENT TEST')
