import datetime


class SearchTerm:
    id: int
    search_term: str
    updated_sentiments_at: datetime

    def __init__(self,
                 search_term_id: int,
                 search_term: str = '',
                 updated_sentiments_at: datetime = None):
        self.id = search_term_id
        self.search_term = search_term
        self.updated_sentiments_at = updated_sentiments_at

    def to_dict(self):
        return vars(self)
