import scrapy


class NewsSpider(scrapy.Spider):
    name = "news_wp"
    page = 1
    MAX_PAGE = 1
    start_urls = [
        'https://wiadomosci.wp.pl/',
    ]

    def parse(self, response):
        articles = response.css("div.j2PrHTUx a::attr('href')").getall()
        yield from response.follow_all(articles, self.parse_article)
        if self.page < self.MAX_PAGE:
            self.page += 1
            url = f"https://wiadomosci.wp.pl/{self.page}"
            yield scrapy.Request(url=url, callback=self.parse)

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
            'title': response.css("h1.article--title ::text").get(),
            'subtitle': response.css("div.article--lead p ::text").get(),
            'publishedAt': response.css("div.signature--when time ::attr('datetime')").get(),
            'author': response.css("span.signature--author ::text").getall()[1],
            'text': extract_all_with_css("div.article--text ::text")
        }
