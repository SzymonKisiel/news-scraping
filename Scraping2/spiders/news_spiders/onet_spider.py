import scrapy


class OnetNewsSpider(scrapy.Spider):
    name = "onet_spider"
    page = 1
    MAX_PAGE = 10
    start_urls = [
        'https://wiadomosci.onet.pl',
        'https://wiadomosci.onet.pl/?ajax=1&page=1'
    ]

    def parse(self, response):
        articles = response.css(".mediumNewsBox::attr(href), .itemBox::attr(href)").getall()
        yield from response.follow_all(articles, self.parse_article)
        if self.page < self.MAX_PAGE:
            self.page += 1
            url = f"https://wiadomosci.onet.pl/?ajax=1&page={self.page}"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_article(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_all_with_css(*queries):
            for query in queries:
                result = ''
                for block in response.css(query).getall():
                    result += block.strip()
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
