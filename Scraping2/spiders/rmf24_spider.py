# h3
import datetime

import scrapy
from scrapy import exceptions
from utils import spider_util


class Rmf24NewsSpider(spider_util.NewsSpider):
    name = "rmf24_spider"
    website = "rmf24"
    delay_setting_name = "DELAY_RMF24"
    # page = 1
    # MAX_PAGE = 20
    start_urls = [
        'https://www.rmf24.pl/fakty'
        # 'https://www.rmf24.pl/fakty,nPack,28804'
    ]

    def __init__(self, category=None, *args, **kwargs):
        super(Rmf24NewsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        articles = response.css("h3 a::attr('href')").getall()
        # test = {}
        yield from response.follow_all(articles, self.parse_article)
        # print(test)
        # print(articles_responses)
        # for i in articles_responses:
        #     print(i)
        # yield from articles_responses

        next_page = response.css("li.next a::attr('href')").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        dt = self.parse_article_datetime(response)
        yield {
            'url': response.url,
            'publishedAt': dt.isoformat(),
            'title': self.extract_with_css(response, "h1.article-title ::text"),
            'author': self.extract_all_with_css(".isAutor ::text"),
            'subtitle': self.extract_with_css(response, "p.article-lead ::text"),
            'text': self.extract_all_with_css(response, "div.articleContent p ::text, div.articleContent h2 ::text")
        }
        # yield {
        #     'url': response.url,
        #     'publishedAt': publishedAt,
        #     'title': extract_with_css("h1.article-title ::text"),
        #     'author': extract_all_with_css(".isAutor ::text"),
        #     'subtitle': extract_with_css("p.article-lead ::text"),
        #     'text': extract_all_with_css("div.articleContent p ::text, div.articleContent h2 ::text")
        # }

    def extract_publish_date(self, response):
        return self.extract_with_css(response, "div.article-date meta[itemprop='datePublished'] ::attr('content')")

