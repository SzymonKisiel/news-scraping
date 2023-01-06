import datetime
import logging
from typing import List
from database.database import get_mysql_db_connection
from models.article import Article


class ArticleRepository:
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def __get_articles(self, query, data, connection=None):
        # Init connection
        if connection is None:
            cnx = get_mysql_db_connection()
        else:
            cnx = connection
        cursor = cnx.cursor()

        # Execute query
        cursor.execute(query, data)

        # Save results
        articles: List[Article] = []
        for (article_id, url, website, published_at, title, author, subtitle, text, created_at) in cursor:
            self.logger.debug(f"{article_id}: {website}; {url}; {title};")
            article = Article(article_id, url, website, published_at, title, author, subtitle, text, created_at)
            articles.append(article)

        # Close the connection
        cursor.close()
        if connection is None:
            cnx.close()

        return articles

    def search(self, word: str, connection=None) -> List[Article]:
        self.logger.debug('search')
        query = """
            SELECT a.id, a.url, a.website, a.published_at, a.title, a.author, a.subtitle, a.`text`, a.created_at 
            FROM news_scraping_db.article AS a
            WHERE a.title LIKE %(word)s OR
                a.subtitle LIKE %(word)s OR
                a.`text` LIKE %(word)s;
        """
        data = {
            "word": "%{}%".format(word),
        }
        return self.__get_articles(query, data, connection)

    def search_created_after(self, word: str, created_after: datetime, connection=None):
        self.logger.debug('search')
        query = """
            SELECT a.id, a.url, a.website, a.published_at, a.title, a.author, a.subtitle, a.`text`, a.created_at 
            FROM news_scraping_db.article AS a
            WHERE (a.title LIKE %(word)s OR
                a.subtitle LIKE %(word)s OR
                a.`text` LIKE %(word)s) AND 
                a.created_at > %(created_after)s;
        """
        data = {
            "word": "%{}%".format(word),
            "created_after": created_after
        }
        return self.__get_articles(query, data, connection)

    def get_all(self, connection=None) -> List[Article]:
        self.logger.debug('get_all')
        query = """
            SELECT a.id, a.url, a.website, a.published_at, a.title, a.author, a.subtitle, a.`text`, a.created_at
            FROM news_scraping_db.article AS a
        """
        return self.__get_articles(query, None, connection)

    def get_by_id(self, article_id) -> Article:
        self.logger.debug('get_by_id')

        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()
        query = ("SELECT id, url, website, published_at, title, author, subtitle, text, created_at "
                 "FROM article "
                 "WHERE id = %s")
        cursor.execute(query, (article_id, ))
        article = cursor.fetchone()

        if article is None:
            self.logger.debug(f"Article with id {article_id} was not found")
        else:
            (article_id, url, published_at, title, author, subtitle, text, website) = article
            self.logger.debug(f"Article with id {article_id} was successfully found")
            self.logger.debug(f"{article}")
            self.logger.debug(f"{article_id}: {website}; {url}; {title};")

        cursor.close()
        cnx.close()

        return article
