import logging
# import mysql.connector
from database.database import get_mysql_db_connection
from database.repositories.articles_repository import ArticlesRepository


class SearchService:
    logger: logging.Logger
    repository: ArticlesRepository

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.articles_repository = ArticlesRepository(logger)

    def get_all_articles(self):
        self.logger.debug('get_all_articles')
        return self.articles_repository.get_all()

    def get_article_by_id(self, article_id):
        self.logger.debug('get_article_by_id')
        return self.articles_repository.get_by_id(article_id)
