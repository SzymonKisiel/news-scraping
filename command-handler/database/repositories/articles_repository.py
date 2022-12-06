import logging
from database.database import get_mysql_db_connection


class ArticlesRepository:
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def get_all(self):
        self.logger.debug('get_all')

        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()
        query = ("SELECT id, url, published_at, title, author, subtitle, text, website "
                 "FROM articles")
        cursor.execute(query)

        articles = []
        for (article_id, url, published_at, title, author, subtitle, text, website) in cursor:
            self.logger.debug(f"{article_id}: {website}; {url}; {title};")
            article = (article_id, url, published_at, title, author, subtitle, text, website)
            articles.append(article)

        cursor.close()
        cnx.close()

        return articles

    def get_by_id(self, article_id):
        self.logger.debug('get_by_id')

        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()
        query = ("SELECT id, url, published_at, title, author, subtitle, text, website "
                 "FROM articles "
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
