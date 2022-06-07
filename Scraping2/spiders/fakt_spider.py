import scrapy
import re
from scrapy.spiders import SitemapSpider

from datetime import datetime
from scrapy.spiders import SitemapSpider

from pytz import timezone
import re
from utils import time_util, spider_util


class FaktNewsSpider(SitemapSpider, spider_util.NewsSpider):
    name = 'fakt_spider'
    website = "fakt"
    delay_setting_name = "DELAY_FAKT"
    allowed_domains = ['fakt.pl']
    sitemap_urls = ['https://www.fakt.pl/sitemap_article.xml']

    date_sitemap_regex = re.escape('https://www.fakt.pl/sitemap_article.xml?nmbr=')
    date_sitemap_format = 'https://www.fakt.pl/sitemap_article.xml?nmbr=%Y%m%d'

    # def __init__(self, category=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.last_crawl_date = time_util.get_last_scraped_date(self.website)
    #     self.last_scraped_date = self.last_crawl_date

    def sitemap_filter(self, entries):
        """
        Filters out days before last crawl
        """
        # debug
        # local = timezone("Poland")
        # dt = datetime.strptime("2022-04-28", "%Y-%m-%d")
        # dt = local.localize(dt)

        dt = self.last_crawl_date
        for entry in entries:
            loc = entry['loc']
            if re.search(self.date_sitemap_regex, loc):
                date_time = datetime.strptime(loc, self.date_sitemap_format)
                if date_time.date() >= dt.date():
                    # print(date_time, "=", dt)
                    yield entry
            else:
                yield entry

    def parse(self, response, **kwargs):
        # 'publishedAt': self.extract_with_css(response, "div.article-date utils ::attr(datetime)"),
        # yield {
        #        'publishedAt': self.extract_with_css(response, "div.article-date time ::attr(datetime)"),
        #        'url': response.url
        #        }
        published_at_str = self.extract_publish_date(response)
        published_at_dt = time_util.string_to_datetime(published_at_str, self.website)
        if published_at_dt <= self.last_crawl_date:
            print(f"not OK: {published_at_dt}")
            return
        else:
            print(f"OK: {published_at_dt}")

        if published_at_dt > self.last_scraped_date:
            self.last_scraped_date = published_at_dt
        yield {
            'url': response.url,
            'publishedAt': published_at_dt.isoformat(),
            'title': self.extract_with_css(response, ".article-title ::text"),
            'author': "",
            'subtitle': self.extract_all_with_css(response, ".article-lead ::text"),
            'text': self.extract_all_with_css(response, ".article .article-p ::text")
        }

    def extract_publish_date(self, response):
        return self.extract_with_css(response, ".article-date ::attr(datetime)")

    def close(self, reason):
        print(f" - - - {self.name} closed - - - ")
        print(f"Spider closed: reached old articles (last published at {self.last_scraped_date})")
        time_util.set_last_scraped_date(self.last_scraped_date, self.website)


# class FaktNewsSpider(SitemapSpider):
#     name = "fakt_spider"
#     allowed_domains = ["fakt.pl"]
#     sitemap_urls = ["https://www.fakt.pl/sitemap_article.xml"]
#     # sitemap_follow = [re.escape("https://www.fakt.pl/sitemap_article.xml?nmbr=20220310")]  # 2022 March 10 articles
#
#     # parse articles found in sitemap
#     def parse(self, response):
#         def extract_with_css(query):
#             return response.css(query).get(default='').strip()
#
#         def extract_all_with_css(query):
#             result = ''
#             for block in response.css(query).getall():
#                 result += block.strip() + " "
#             return result
#
#         yield {
#             'url': response.url,
#             'publishedAt': extract_with_css("div.article-date utils ::attr(datetime)"),
#             'title': extract_with_css("h1.article-title ::text"),
#             'author': "",
#             'subtitle': extract_all_with_css("div.article-lead ::text"),
#             'text': extract_all_with_css(".article .article-p ::text")
#         }
#
#     def closed(self, reason):
#         print(f" - - - {self.name} closed - - - ")
#         print(f"Spider closed: reached old articles (last published at {self.last_scraped_date})")
#         time_util.set_last_scraped_date(self.last_scraped_date, self.website)
