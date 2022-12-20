import logging
from typing import List

from database.database import get_mysql_db_connection
from models.client import Client


class ClientRepository:
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def get_all_clients(self) -> List[Client]:
        self.logger.debug('get_all_clients')

        # Init connection
        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()

        # Prepare query and data
        query = ("SELECT id, name "
                 "FROM client")

        # Execute query
        cursor.execute(query)

        # Save results
        clients: List[Client] = []
        for (id, name) in cursor:
            self.logger.debug(f"{id}: {name}")
            client = Client(id, name)
            clients.append(client)

        # Close the connection
        cursor.close()
        cnx.close()

        return clients

    def add_client(self, client_name):
        self.logger.debug('get_all_clients')

        # Init connection
        cnx = get_mysql_db_connection()
        cursor = cnx.cursor()

        # Prepare statement and data
        statement = """
            INSERT INTO news_scraping_db.client
                (name)
            VALUES
                (%(client_name)s);
        """
        data = {
            'client_name': client_name
        }

        # Execute query and save results
        cursor.execute(statement, data)

        # Make sure data is committed to the database and close the connection
        cnx.commit()
        cursor.close()
        cnx.close()
