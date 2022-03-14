# h3

import scrapy


class Rmf24NewsSpider(scrapy.Spider):
    name = "rmf24_spider"
    page = 1
    MAX_PAGE = 20
    start_urls = [
        'https://www.rmf24.pl/fakty'
    ]

    def parse(self, response):
        articles = response.css("h3 a::attr('href')").getall()
        yield from response.follow_all(articles, self.parse_article)
        if self.page < self.MAX_PAGE:
            self.page += 1
            next_page = response.css("li.next a::attr('href')").get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_all_with_css(query):
            result = ''
            for block in response.css(query).getall():
                result += block.strip()
            return result

        yield {
            'url': response.url,
            'publishedAt': extract_with_css("div.article-date meta[itemprop='datePublished'] ::attr('content')"),
            'title': extract_with_css("h1.article-title ::text"),
            'author': extract_with_css("span.article-author-name ::text"),
            'subtitle': extract_with_css("p.article-lead ::text"),
            'text': extract_all_with_css("div.articleContent p ::text, div.articleContent h2 ::text")
        }
