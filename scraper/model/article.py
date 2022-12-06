import datetime


class Article:
    url: str
    published_at: datetime
    title: str
    author: str
    subtitle: str
    text: str

    def __init__(self, item):
        self.url = item['url']
        self.published_at = item['published_at']
        self.title = item['title']
        self.author = item['author']
        self.subtitle = item['subtitle']
        self.text = item['text']
