import logging
from typing import List
from database.database import get_mysql_db_connection
from models.search_term import SearchTerm


class SearchTermRepository:
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def __get_search_terms(self, query, data):
        # Init connection
        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()

        # Execute query
        cursor.execute(query, data)

        # Save results
        search_terms: List[SearchTerm] = []
        for (id, name, updated_sentiments_at) in cursor:
            self.logger.debug(f"{id}; {name}; {updated_sentiments_at}")
            search_term = SearchTerm(id, name, updated_sentiments_at)
            search_terms.append(search_term)

        # Close the connection
        cursor.close()
        cnx.close()

        return search_terms

    def get_all_by_client_id(self, client_id) -> List[SearchTerm]:
        self.logger.debug('get_all_by_client_id')
        query = """
            SELECT st.id, st.term, st.updated_sentiments_at
            FROM news_scraping_db.client AS c
            JOIN news_scraping_db.client_search_term AS c_st ON c.id = c_st.client_id
            JOIN news_scraping_db.search_term AS st ON c_st.search_term_id = st.id
            WHERE c.id = %(client_id)s;
        """
        data = {
            "client_id": client_id
        }
        return self.__get_search_terms(query, data)

    def get_all_by_client_name(self, client_name) -> List[SearchTerm]:
        self.logger.debug('get_all_by_client_name')
        query = """
            SELECT st.id, st.term, st.updated_sentiments_at
            FROM news_scraping_db.client AS c
            JOIN news_scraping_db.client_search_term AS c_st ON c.id = c_st.client_id
            JOIN news_scraping_db.search_term AS st ON c_st.search_term_id = st.id
            WHERE c.name = %(client_name)s;
        """
        data = {
            "client_name": client_name
        }
        return self.__get_search_terms(query, data)

    def add_search_term_to_client(self, client_name, search_term):
        self.logger.debug('add_search_term_to_client')

        # Init connection
        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()

        # Execute procedure - can throw DatabaseError
        cursor.callproc('AddSearchTerm', args=(client_name, search_term))

        # Close the connection
        cnx.commit()
        cursor.close()
        cnx.close()
