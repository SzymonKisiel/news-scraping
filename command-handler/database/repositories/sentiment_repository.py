import logging
from typing import List
from database.database import get_mysql_db_connection
from models.article import Article
from models.search_term import SearchTerm
from models.sentiment import Sentiment


class SentimentRepository:
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def __get_sentiments(self, query, data) -> List[Sentiment]:
        # Init connection
        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()

        # Execute query
        cursor.execute(query, data)

        # Save results
        sentiments: List[SearchTerm] = []
        for (id, article_id, search_term_id, sentence,
             positive_score, neutral_score, negative_score, overall_sentiment,
             art_url, art_website, art_published_at, art_title, art_author, art_subtitle, art_text, art_created_at,
             search_term_name, search_term_updated_at) in cursor:
            self.logger.debug(f"{id}: {art_title}, {positive_score}, {neutral_score}, {negative_score}")
            sentiment = Sentiment(
                id=id,
                article_id=article_id,
                article=Article(
                    article_id,
                    url=art_url,
                    website=art_website,
                    published_at=art_published_at,
                    title=art_title,
                    author=art_author,
                    subtitle=art_subtitle,
                    text=art_text,
                    created_at=art_created_at
                ),
                search_term_id=search_term_id,
                search_term=SearchTerm(
                    search_term_id,
                    search_term=search_term_name,
                    updated_sentiments_at=search_term_updated_at
                ),
                sentence=sentence,
                positive_score=positive_score,
                neutral_score=neutral_score,
                negative_score=negative_score,
                overall_sentiment=overall_sentiment
            )
            sentiments.append(sentiment)

        # Close the connection
        cursor.close()
        cnx.close()

        return sentiments

    def get_all_by_client_id(self, client_id):
        self.logger.debug(f"get_all_by_client_id: {client_id}")
        query = """
            SELECT s.id, s.article_id, s.search_term_id, s.sentence, s.positive_score, s.neutral_score, s.negative_score, s.overall_sentiment,
                a.url, a.website, a.published_at, a.title, a.author, a.subtitle, a.`text`, a.created_at,
                st.term, st.updated_sentiments_at
            FROM news_scraping_db.sentiment s
            JOIN news_scraping_db.sentiment_label sl ON s.overall_sentiment = sl.id
            JOIN news_scraping_db.article a ON s.article_id = a.id
            JOIN news_scraping_db.search_term st ON s.search_term_id = st.id
            JOIN news_scraping_db.client_search_term cst ON st.id = cst.search_term_id
            JOIN news_scraping_db.client c ON cst.client_id = c.id
            WHERE c.id = %(client_id)s
            ORDER BY a.published_at;
        """
        data = {
            "client_id": client_id
        }
        return self.__get_sentiments(query, data)

    def get_all_by_client_name(self, client_name):
        self.logger.debug(f"get_all_by_client_name: {client_name}")
        query = """
            SELECT s.id, s.article_id, s.search_term_id, s.sentence, s.positive_score, s.neutral_score, s.negative_score, s.overall_sentiment,
                a.url, a.website, a.published_at, a.title, a.author, a.subtitle, a.`text`, a.created_at,
                st.term, st.updated_sentiments_at
            FROM news_scraping_db.sentiment s
            JOIN news_scraping_db.sentiment_label sl ON s.overall_sentiment = sl.id
            JOIN news_scraping_db.article a ON s.article_id = a.id
            JOIN news_scraping_db.search_term st ON s.search_term_id = st.id
            JOIN news_scraping_db.client_search_term cst ON st.id = cst.search_term_id
            JOIN news_scraping_db.client c ON cst.client_id = c.id
            WHERE c.name = %(client_name)s
            ORDER BY a.published_at;
        """
        data = {
            "client_name": client_name
        }
        return self.__get_sentiments(query, data)

    def get_all_by_search_term_id(self, search_term_id):
        self.logger.debug(f"get_all_by_search_term_id: {search_term_id}")
        query = """
            SELECT s.id, s.article_id, s.search_term_id, s.sentence, s.positive_score, s.neutral_score, s.negative_score, s.overall_sentiment,
                a.url, a.website, a.published_at, a.title, a.author, a.subtitle, a.`text`, a.created_at,
                st.term, st.updated_sentiments_at
            FROM news_scraping_db.sentiment s
            JOIN news_scraping_db.sentiment_label sl ON s.overall_sentiment = sl.id
            JOIN news_scraping_db.article a ON s.article_id = a.id
            JOIN news_scraping_db.search_term st ON s.search_term_id = st.id
            WHERE st.id = %(search_term_id)s
            ORDER BY a.published_at;
        """
        data = {
            "search_term_id": search_term_id
        }
        return self.__get_sentiments(query, data)

    def get_all_by_search_term_name(self, search_term_name):
        self.logger.debug(f"get_all_by_search_term_name: {search_term_name}")
        query = """
            SELECT s.id, s.article_id, s.search_term_id, s.sentence, s.positive_score, s.neutral_score, s.negative_score, s.overall_sentiment,
                a.url, a.website, a.published_at, a.title, a.author, a.subtitle, a.`text`, a.created_at,
                st.term, st.updated_sentiments_at
            FROM news_scraping_db.sentiment s
            JOIN news_scraping_db.sentiment_label sl ON s.overall_sentiment = sl.id
            JOIN news_scraping_db.article a ON s.article_id = a.id
            JOIN news_scraping_db.search_term st ON s.search_term_id = st.id
            WHERE st.term = %(search_term_name)s
            ORDER BY a.published_at;
        """
        data = {
            "search_term_name": search_term_name
        }
        return self.__get_sentiments(query, data)

    def insert_sentiment(self, sentiment: Sentiment, connection=None):
        self.logger.debug('insert_sentiment')

        # Init connection
        if connection is None:
            cnx = get_mysql_db_connection()
        else:
            cnx = connection
        cursor = cnx.cursor()

        # Prepare statement and data
        statement = """
            INSERT INTO news_scraping_db.sentiment
                (article_id, search_term_id, sentence, positive_score, neutral_score, negative_score, overall_sentiment)
            VALUES
                (%(article_id)s, %(search_term_id)s, %(sentence)s, %(positive_score)s, %(neutral_score)s, %(negative_score)s, %(overall_sentiment)s);
        """
        data = {
            'article_id': sentiment.article_id,
            'search_term_id': sentiment.search_term_id,
            'sentence': sentiment.sentence,
            'positive_score': sentiment.positive_score,
            'neutral_score': sentiment.neutral_score,
            'negative_score': sentiment.negative_score,
            'overall_sentiment': sentiment.overall_sentiment
        }

        # Execute query and save results
        cursor.execute(statement, data)

        # Make sure data is committed to the database and close the connection
        if connection is None:
            cnx.commit()
        cursor.close()
        if connection is None:
            cnx.close()

    def count_sentiments(self, article_id, search_term_id) -> int:
        # Init connection
        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()

        # Prepare query and data
        query = """
            SELECT COUNT(*)
            FROM news_scraping_db.sentiment s
            JOIN news_scraping_db.sentiment_label sl ON s.overall_sentiment = sl.id
            JOIN news_scraping_db.article a ON s.article_id = a.id
            JOIN news_scraping_db.search_term st ON s.search_term_id = st.id
            WHERE a.id = %(article_id)s AND st.id = %(search_term_id)s;
        """
        data = {
            "article_id": article_id,
            "search_term_id": search_term_id
        }

        # Execute query
        cursor.execute(query, data)
        (count,) = cursor.fetchone()
        self.logger.debug(f"count: {count}")

        # Close the connection
        cursor.close()
        cnx.close()

        return count
