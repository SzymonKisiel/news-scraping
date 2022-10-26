import scrapy
from settings.last_article_dates import get_last_scraped_date, set_last_scraped_date
from utils import time_util
from scrapy.exceptions import CloseSpider


class NewsSpider(scrapy.Spider):
    """
    Spider
    """
    website = "test"

    def __init__(self, category=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_crawl_date = get_last_scraped_date(self.website)
        self.last_scraped_date = self.last_crawl_date

        print(f"Spider {self.name} started")

    def extract_with_css(self, response, query):
        return response.css(query).get(default='').strip()

    # def extract_all_with_css(self, response, query):
    #     result = ''
    #     for block in response.css(query).getall():
    #         result += block.strip() + " "
    #     return result

    def extract_all_with_css(self, response, *queries):
        for query in queries:
            result = ''
            for block in response.css(query).getall():
                result += block.strip() + " "
            if result != '':
                return result

    def extract_publish_date(self, response):
        raise scrapy.exceptions.CloseSpider("Not implemented")

    def parse_article_datetime(self, response):
        published_at = self.extract_publish_date(response)
        dt = time_util.string_to_datetime(published_at, self.website)

        if dt <= self.last_crawl_date:
            raise CloseSpider("Reached old articles")
        else:
            pass  # print(f"OK: {dt}")

        if dt > self.last_scraped_date:
            self.last_scraped_date = dt
        return dt

    def closed(self, reason):
        if reason == "Reached old articles":
            print(f"Spider {self.name} closed: reached old articles (last published at {self.last_scraped_date})")
            set_last_scraped_date(self.last_scraped_date, self.website)
        elif reason == "Not implemented":
            raise NotImplementedError
        else:
            print(f"Spider {self.name} closed")
