from datetime import datetime


class Article:
    article_id: int
    url: str
    website: str
    published_at: datetime
    title: str
    author: str
    subtitle: str
    text: str
    created_at: datetime

    def __init__(self,
                 article_id: int,
                 url: str = '',
                 website: str = '',
                 published_at: datetime = datetime.min,
                 title: str = '',
                 author: str = '',
                 subtitle: str = '',
                 text: str = '',
                 created_at: datetime = None):
        self.article_id = article_id
        self.url = url
        self.website = website
        self.published_at = published_at
        self.title = title if title is not None else ''
        self.author = author
        self.subtitle = subtitle if subtitle is not None else ''
        self.text = text if text is not None else ''
        self.created_at = created_at

    def to_dict(self):
        return vars(self)
