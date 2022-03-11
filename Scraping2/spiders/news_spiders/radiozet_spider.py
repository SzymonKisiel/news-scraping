import scrapy
#test = response.css(".radiozet-footer__top a::attr('href')").getall()

class RadiozetNewsSpider(scrapy.Spider):
    name = "radiozet_spider"
    page = 1
    MAX_PAGE = 1
    start_urls = [
        'https://www.radiozet.pl',
    ]

    def parse(self, response):
        categories = response.css("div.radiozet-footer__top a::attr('href')").getall()

        # # debug
        # for category in categories:
        #     print(category)
        # yield {"url": response.url}
        # categories = categories[1:2]

        yield from response.follow_all(categories, self.parse_categories)

    def parse_categories(self, response):
        articles = response.css("div.list-element__title a::attr('href')").getall()
        yield from response.follow_all(articles, self.parse_article)
        if self.page < self.MAX_PAGE:
            self.page += 1
            next_page = response.css("a.pagination__button--next ::attr('href')").get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_categories)

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
            'subtitle': extract_all_with_css("div.full__article__lead p ::text"),
            'text': extract_all_with_css("div.full__article__body p ::text, div.full_article__body h2 ::text")
        }
