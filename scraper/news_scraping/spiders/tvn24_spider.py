# https://www.tvp.info/swiat
# class="main-mesh-box__text-container box__text-container"
# main-mesh-box__text-container box__text-container
# main-mesh-box__text-container box__text-container
import scrapy
from utils import spider_util
from utils import time_util


class Tvn24NewsSpider(spider_util.NewsSpider):
    name = "tvn24_spider"
    website = "tvn24"
    delay_setting_name = "DELAY_TVN24"
    page = 1
    start_urls = [
        f"https://tvn24.pl/najnowsze/{page}"
        # 'https://tvn24.pl/najnowsze'
        # 'https://tvn24.pl/najnowsze/320'
        # 'https://tvn24.pl/najnowsze/50000'
    ]
    custom_settings = {
        'HTTPERROR_ALLOWED_CODES': [500]
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skipped_pages = []
        self.skipped_articles = []

    def parse(self, response):
        if response.status == 500:
            self.crawler.stats.inc_value('skipped_page_count')
            self.skipped_pages.append(response.url)
            self.page += 1
            yield scrapy.Request(f"https://tvn24.pl/najnowsze/{self.page}", callback=self.parse)
        else:
            articles = response.css("article div div a::attr('href')").getall()
            if articles:
                yield from response.follow_all(articles, self.parse_article)
                self.page += 1
                yield scrapy.Request(f"https://tvn24.pl/najnowsze/{self.page}", callback=self.parse)

        # if self.page < self.MAX_PAGE:
        #     self.page += 1
        #     url = f"https://tvn24.pl/najnowsze/{self.page}"
        #     yield scrapy.Request(url=url, callback=self.parse)

        # self.page += 1
        # next_page = scrapy.Request(f"https://tvn24.pl/najnowsze/{self.page}")
        # if next_page is not None:
        #     yield from response.follow(next_page, self.parse)

    def parse_article(self, response):
        if response.status == 500:
            self.crawler.stats.inc_value('skipped_article_count')
            self.skipped_articles.append(response.url)

        dt = self.parse_article_datetime(response)
        if dt is None:
            return

        yield {
            'url': response.url,
            'published_at': dt.isoformat(),
            'title': self.extract_with_css(response, "h1.heading ::text"),
            'author': self.extract_with_css(response, "div.author-first-name ::text"),
            'subtitle': self.extract_with_css(response, ".article-element--lead_text ::text"),
            'text': self.extract_all_with_css(response, ".article-element--paragraph ::text,"
                                                        ".article-element--subhead ::text")
        }

    def extract_publish_date(self, response):
        meta_date = self.extract_with_css(response, ".article__content__meta-date ::attr(datetime)")
        bar_date = self.extract_with_css(response, ".article-top-bar__date ::attr(datetime)")
        
        # to refactor - publish date scraping
        if not bar_date:
            return meta_date
        if not meta_date:
            return bar_date

        bar_date = bar_date[:-1]

        if meta_date == bar_date:
            return meta_date

        meta_dt = time_util.string_to_datetime(meta_date, self.website)
        bar_dt = time_util.string_to_datetime(bar_date, self.website)

        if meta_dt >= bar_dt:
            return meta_date
        else:
            return bar_date

        # return self.extract_with_css(response, ".article__content__meta-date ::attr(datetime)")
        # return self.extract_with_css(response, ".article-top-bar__date ::attr(datetime)")
        # return self.extract_with_css(response, "utils.article-top-bar__date ::attr('datetime')")

    def closed(self, reason):
        super().closed(reason)
        self.crawler.stats.set_value('skipped_pages', ', '.join(self.skipped_pages))
        self.crawler.stats.set_value('skipped_articles', ', '.join(self.skipped_articles))
