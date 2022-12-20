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

    def __init__(self,
                 article_id,
                 url='',
                 website='',
                 published_at=datetime.now(),
                 title='',
                 author='',
                 subtitle='',
                 text=''):
        self.article_id = article_id
        self.url = url
        self.website = website
        self.published_at = published_at
        self.title = title if title is not None else ''
        self.author = author
        self.subtitle = subtitle if subtitle is not None else ''
        self.text = text if text is not None else ''
