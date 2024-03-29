from typing import List
from models.search_term import SearchTerm


class Client:
    id: int
    name: str
    search_terms: List[SearchTerm]

    def __init__(self,
                 id: int,
                 name: str = ''):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
