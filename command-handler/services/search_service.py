import logging
# import mysql.connector
from database.database import get_mysql_db_connection
from database.repositories.article_repository import ArticleRepository


class SearchService:
    logger: logging.Logger
    repository: ArticleRepository

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.article_repository = ArticleRepository(logger)

    def search(self, word: str):
        self.logger.debug('get_all_articles')
        articles = self.article_repository.search(word)
        for article in articles:
            text = article.title + article.subtitle + article.text
            sentences = [sentence + '.' for sentence in text.split('.') if word in sentence]
            self.logger.debug(sentences)

    def get_all_articles(self):
        self.logger.debug('get_all_articles')
        return self.article_repository.get_all()

    def get_article_by_id(self, article_id):
        self.logger.debug('get_article_by_id')
        return self.article_repository.get_by_id(article_id)
