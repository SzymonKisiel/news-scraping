from utils import spider_util, time_util
from settings.last_article_dates import set_last_scraped_date


class CloseCategory(Exception):
    """Stop crawling category"""
    pass


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

    def __init__(self, category=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stop_following_links_in_category = {}

    def parse(self, response):
        categories = response.css("div.radiozet-footer__top a::attr('href')").getall()

        # debug
        categories = categories[1:3]
        for category in categories:
            # print(category)
            # init dictionary
            self.stop_following_links_in_category[category] = False

            yield response.follow(category, self.parse_category, cb_kwargs={'category': category})

        # yield from response.follow_all(categories, self.parse_category)

    def parse_category(self, response, category):
        articles = response.css("div.list-element__title a::attr('href')").getall()
        # yield from response.follow_all(articles, self.parse_article)

        for article in articles:
            if self.stop_following_links_in_category[category]:
                break
            else:
                yield response.follow(article, self.parse_article, cb_kwargs={'category': category})
        if not self.stop_following_links_in_category[category]:
            next_page = response.css("a.pagination__button--next ::attr('href')").get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_category, cb_kwargs={'category': category})

    def parse_article_datetime(self, response):
        published_at = self.extract_publish_date(response)
        dt = time_util.string_to_datetime(published_at, self.website)
        if dt <= self.last_crawl_date:
            raise CloseCategory
        else:
            pass #print(f"OK: {dt}")

        if dt > self.last_scraped_date:
            self.last_scraped_date = dt
        return dt

    def parse_article(self, response, category):
        try:
            dt = self.parse_article_datetime(response)
        except CloseCategory as err:
            # stop parsing category
            self.stop_following_links_in_category[category] = True
        else:
            yield {
                'url': response.url,
                'published_at': dt.isoformat(),
                'title': self.extract_with_css(response, "h1.full__header__title ::text"),
                'author': self.extract_all_with_css(response, "div.info-header__author ::text"),
                'subtitle': self.extract_all_with_css(response, "div.full__article__lead ::text"),
                'text': self.extract_all_with_css(response, "div.full__article__body p ::text, "
                                                            "div.full__article__body h2 ::text,"
                                                            "div.full__article__body ul ::text")
            }

    def extract_publish_date(self, response):
        return self.extract_with_css(response, "div.info-header__date--published ::attr('data-date')")

    def closed(self, reason):
        print(f"Spider {self.name} closed: reached old articles (last published at {self.last_scraped_date})")
        set_last_scraped_date(self.last_scraped_date, self.website)
