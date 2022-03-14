import scrapy
#test = response.css(".radiozet-footer__top a::attr('href')").getall()

class RadiozetNewsSpider(scrapy.Spider):
    name = "radiozet_spider"
    page = 1
    MAX_PAGE = 2
    start_urls = [
        'https://wiadomosci.radiozet.pl'
        #'https://www.radiozet.pl',
    ]
    # allowed_domains = [
    #     'wiadomosci.radiozet.pl'
    # ]

    def parse(self, response):
        categories = response.css("div.radiozet-footer__top a::attr('href')").getall()

        # debug
        categories = categories[1:3]
        # for category in categories:
        #     print(category)

        yield from response.follow_all(categories, self.parse_category)

    def parse_category(self, response):
        articles = response.css("div.list-element__title a::attr('href')").getall()
        yield from response.follow_all(articles, self.parse_article)
        if self.page < self.MAX_PAGE:
            self.page += 1
            next_page = response.css("a.pagination__button--next ::attr('href')").get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_category)

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
            'publishedAt': extract_with_css("div.info-header__date--published ::attr('data-date')"),
            'title': extract_with_css("h1.full__header__title ::text"),
            'author': extract_all_with_css("div.info-header__author ::text"),
            'subtitle': extract_all_with_css("div.full__article__lead ::text"),
            'text': extract_all_with_css("div.full__article__body p ::text, div.full__article__body h2 ::text, "
                                         "div.full__article__body ul ::text")
        }
