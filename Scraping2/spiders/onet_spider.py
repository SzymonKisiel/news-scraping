# response.css(".archiveDay ::attr(href)").getall()
# response.css(".itemTitle ::attr(href)").getall()

import scrapy


class OnetNewsSpider(scrapy.Spider):
    name = "onet_spider"
    start_urls = [
        'https://wiadomosci.onet.pl/mapa-serwisu'
    ]

    def parse(self, response):
        archive_days = response.css(".archiveDay ::attr(href)").getall()
        yield from response.follow_all(archive_days, self.parse_day)

    def parse_day(self, response):
        articles = response.css(".itemTitle ::attr(href)").getall()
        yield from response.follow_all(articles, self.parse_article)

    def parse_article(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        # returns text for first matched query
        def extract_all_with_css(*queries):
            for query in queries:
                result = ''
                for block in response.css(query).getall():
                    result += block.strip() + " "
                if result != '':
                    return result

        yield {
            'url': response.url,
            'publishedAt': extract_with_css("div.dates meta ::attr(content)"),
            'title': extract_with_css("h1.mainTitle ::text"),
            'author': extract_all_with_css(".authDesc ::text", ".authorItem ::text"),
            'subtitle': extract_all_with_css("#lead ::text"),
            'text': extract_all_with_css(".articleDetail p ::text, .articleDetail h2 ::text")
        }
