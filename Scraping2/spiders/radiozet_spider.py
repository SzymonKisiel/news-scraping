import scrapy
from utils import spider_util


# test = response.css(".radiozet-footer__top a::attr('href')").getall()


class RadiozetNewsSpider(spider_util.NewsSpider):
    name = "radiozet_spider"
    website = "radiozet"
    delay_setting_name = "DELAY_RADIOZET"
    # page = 1
    # MAX_PAGE = 2
    start_urls = [
        'https://wiadomosci.radiozet.pl'
        # 'https://www.radiozet.pl',
    ]

    # allowed_domains = [
    #     'wiadomosci.radiozet.pl'
    # ]

    def parse(self, response):
        categories = response.css("div.radiozet-footer__top a::attr('href')").getall()

        # debug
        categories = categories[1:3]
        for category in categories:
            print(category)

        yield from response.follow_all(categories, self.parse_category)

    def parse_category(self, response):
        articles = response.css("div.list-element__title a::attr('href')").getall()
        yield from response.follow_all(articles, self.parse_article)
        # if self.page < self.MAX_PAGE:
        #     self.page += 1
        #     next_page = response.css("a.pagination__button--next ::attr('href')").get()
        #     if next_page is not None:
        #         yield response.follow(next_page, callback=self.parse_category)
        next_page = response.css("a.pagination__button--next ::attr('href')").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_category)

    def parse_article(self, response):
        dt = self.parse_article_datetime(response)
        yield {
            'url': response.url,
            'publishedAt': dt.isoformat(),
            'title': self.extract_with_css(response, "h1.full__header__title ::text"),
            'author': self.extract_all_with_css(response, "div.info-header__author ::text"),
            'subtitle': self.extract_all_with_css(response, "div.full__article__lead ::text"),
            'text': self.extract_all_with_css(response, "div.full__article__body p ::text, "
                                                        "div.full__article__body h2 ::text,"
                                                        "div.full__article__body ul ::text")
        }

    def extract_publish_date(self, response):
        return self.extract_with_css(response, "div.info-header__date--published ::attr('data-date')")
