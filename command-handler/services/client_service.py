import logging
from database.repositories.client_repository import ClientRepository
from database.repositories.search_term_repository import SearchTermRepository
from services.models import AddClientRequest, AddSearchTermRequest


class ClientService:
    logger: logging.Logger
    client_repository: ClientRepository
    search_term_repository: SearchTermRepository

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.client_repository = ClientRepository(logger)
        self.search_term_repository = SearchTermRepository(logger)

    def get_all(self):
        return self.client_repository.get_all_clients()

    def add_client(self, request: AddClientRequest):
        self.client_repository.add_client(request.client_name)

    def add_search_term(self, request: AddSearchTermRequest):
        self.search_term_repository.add_search_term_to_client(request.client_name, request.search_term)
