from typing import List
from models.search_term import SearchTerm


class Client:
    id: int
    name: str
    search_terms: List[SearchTerm]

    def __init__(self,
                 id: int,
                 name: str = '',
                 search_terms: List[SearchTerm] = []):
        self.id = id
        self.name = name
        self.search_terms = search_terms
