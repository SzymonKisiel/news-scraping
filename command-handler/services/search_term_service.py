import logging
from database.repositories.search_term_repository import SearchTermRepository


class SearchTermService:
    logger: logging.Logger
    search_term_repository: SearchTermRepository

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.search_term_repository = SearchTermRepository(logger)

    def get_all_by_client_name(self, client_name: str):
        return self.search_term_repository.get_all_by_client_name(client_name)

    def get_all_by_client_id(self, client_id: int):
        return self.search_term_repository.get_all_by_client_id(client_id)
