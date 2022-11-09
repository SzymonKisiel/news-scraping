import datetime

import scrapy

from utils.spider_util import NewsSpider
from utils.time_util import string_to_datetime
from settings.onet_cookies import get_onet_cookies
from modules.set_scraping_start import set_last_scraped_date
from pytz import timezone


class OnetNewsSpider(NewsSpider):
    name = "onet_spider"
    website = "onet"
    delay_setting_name = "DELAY_ONET"
    start_urls = [
        'https://wiadomosci.onet.pl/mapa-serwisu'
    ]

    def parse(self, response):
        archive_days = response.css(".archiveDay ::attr(href)").getall()
        local = timezone("Poland")
        for archive_day in archive_days:
            archive_day_str = archive_day[10:]
            dt = datetime.datetime.strptime(archive_day_str, "%Y-%m-%d")
            dt = local.localize(dt)
            if dt.date() >= self.last_crawl_date.date():
                yield response.follow(archive_day, self.parse_day, cb_kwargs={'day_str': archive_day_str})

    def parse_day(self, response, day_str):
        articles = response.css(".itemTitle ::attr(href)").getall()
        times_str = response.css(".itemTime ::text").getall()
        local = timezone("Poland")

        for article, time_str in zip(articles, times_str):
            dt = datetime.datetime.strptime(day_str + time_str, "%Y-%m-%d %H:%M")
            dt = local.localize(dt)
            if dt >= self.last_crawl_date:
                onet_cookies = get_onet_cookies()
                yield response.follow(article, self.parse_article,
                                      meta={
                                          'dont_redirect': True,
                                          "handle_httpstatus_list": [302],
                                      },
                                      cookies=onet_cookies)

    def parse_article(self, response):
        # print(f"[{response.status}] {response.url}")
        published_at_str = self.extract_publish_date(response)
        published_at_dt = string_to_datetime(published_at_str, self.website)
        if published_at_dt <= self.last_crawl_date:
            return
        else:
            pass

        if published_at_dt > self.last_scraped_date:
            self.last_scraped_date = published_at_dt

        yield {
            'url': response.url,
            'published_at': published_at_dt.isoformat(),
            'title': self.extract_with_css(response, "h1.mainTitle ::text"),
            'author': self.extract_all_with_css(response, ".authDesc ::text", ".authorItem ::text"),
            'subtitle': self.extract_all_with_css(response, "#lead ::text"),
            'text': self.extract_all_with_css(response, ".articleDetail p ::text, .articleDetail h2 ::text")
        }

    def extract_publish_date(self, response):
        return self.extract_with_css(response, "meta[property='article:published_time'] ::attr(content)")

    def closed(self, reason):
        print(f"Spider {self.name} closed: reached old articles (last published at {self.last_scraped_date})")
        set_last_scraped_date(self.last_scraped_date, self.website)
