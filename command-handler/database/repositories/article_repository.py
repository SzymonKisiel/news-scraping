import logging
from typing import List
from database.database import get_mysql_db_connection
from models.article import Article


class ArticleRepository:
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def __get_articles(self, query, data):
        # Init connection
        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()

        # Execute query
        cursor.execute(query, data)

        # Save results
        articles: List[Article] = []
        for (article_id, url, website, published_at, title, author, subtitle, text) in cursor:
            self.logger.debug(f"{article_id}: {website}; {url}; {title};")
            article = Article(article_id, url, website, published_at, title, author, subtitle, text)
            articles.append(article)

        # Close the connection
        cursor.close()
        cnx.close()

        return articles

    def search(self, word: str) -> List[Article]:
        self.logger.debug('search')
        query = ("SELECT id, url, website, published_at, title, author, subtitle, text "
                 "FROM article "
                 "WHERE title LIKE %(word)s OR "
                 "  subtitle LIKE %(word)s OR "
                 "  `text` LIKE %(word)s;")
        data = {
            "word": "%{}%".format(word),
        }
        return self.__get_articles(query, data)

    def get_all(self) -> List[Article]:
        self.logger.debug('get_all')
        query = """
            SELECT id, url, published_at, title, author, subtitle, text, website
            FROM news_scraping_db.article
        """
        return self.__get_articles(query, None)

    def get_by_id(self, article_id) -> Article:
        self.logger.debug('get_by_id')

        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()
        query = ("SELECT id, url, published_at, title, author, subtitle, text, website "
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
