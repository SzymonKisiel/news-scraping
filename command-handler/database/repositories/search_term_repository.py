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

    def __get_search_term(self, query, data):
        # Init connection
        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()

        # Execute query
        cursor.execute(query, data)

        # Save result
        result = cursor.fetchone()

        if result is None:
            self.logger.debug(f"Search term was not found")
        else:
            (id, name, updated_sentiments_at) = result
            search_term = SearchTerm(id, name, updated_sentiments_at)
            self.logger.debug(f"Search term with id {search_term.id} was successfully found")
            self.logger.debug(f"{search_term.id}: {search_term.search_term}; {search_term.updated_sentiments_at}")

        # Close the connection
        cursor.close()
        cnx.close()

        return search_term

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

    def get_by_search_term_name(self, search_term_name) -> SearchTerm:
        self.logger.debug('get_by_search_term_name')
        query = """
            SELECT st.id, st.term, st.updated_sentiments_at
            FROM news_scraping_db.search_term AS st 
            WHERE st.term = %(search_term_name)s;
        """
        data = {
            "search_term_name": search_term_name
        }
        return self.__get_search_term(query, data)

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

    def add_search_term_to_client_by_id(self, client_id, search_term):
        self.logger.debug('add_search_term_to_client')

        # Init connection
        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()

        # Execute procedure - can throw DatabaseError
        cursor.callproc('AddSearchTermById', args=(client_id, search_term))

        # Close the connection
        cnx.commit()
        cursor.close()
        cnx.close()

    def get_all_search_terms(self):
        self.logger.debug('get_all_search_terms')
        query = """
            SELECT st.id, st.term, st.updated_sentiments_at
            FROM news_scraping_db.search_term AS st;
        """
        return self.__get_search_terms(query, None)

    def set_term_updated_sentiments_at(self, search_term_id, new_timestamp, connection=None):
        # Init connection
        if connection is None:
            cnx = get_mysql_db_connection()
        else:
            cnx = connection
        cursor = cnx.cursor()

        # Prepare statement and data
        statement = """
            UPDATE news_scraping_db.search_term
            SET updated_sentiments_at = %(new_timestamp)s
            WHERE id = %(search_term_id)s;
        """
        data = {
            "new_timestamp": new_timestamp,
            "search_term_id": search_term_id
        }

        # Execute query and save results
        cursor.execute(statement, data)

        # Make sure data is committed to the database and close the connection
        if connection is None:
            cnx.commit()
        cursor.close()
        if connection is None:
            cnx.close()
