import scrapy
from settings.last_article_dates import get_last_scraped_date, set_last_scraped_date
from utils import time_util
from scrapy.exceptions import CloseSpider
from scrapy.spiders import SitemapSpider
from scrapy.http import Request
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots
from scrapy.spiders.sitemap import iterloc, logger
from settings.onet_cookies import get_onet_cookies


class NewsSpider(scrapy.Spider):
    """
    Spider
    """
    website = "test"
    bugged_dt = time_util.string_to_datetime('2022-10-10T10:30:00+02:00')
    stop_date = None
    

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

        # tvn24 bug workaround
        if self.bugged_dt == dt:
            return None

        if dt <= self.last_crawl_date:
            self.stop_date = dt
            raise CloseSpider("Reached old articles")
        else:
            pass  # print(f"OK: {dt}")

        if dt > self.last_scraped_date:
            self.last_scraped_date = dt
        return dt

    def closed(self, reason):
        if reason == "Reached old articles":
            self.crawler.stats.set_value('last_published_at', self.last_scraped_date)
            self.crawler.stats.set_value('stop_published_at', self.stop_date)
            print(f"Spider {self.name} closed: reached old articles (last published at {self.last_scraped_date})")
            set_last_scraped_date(self.last_scraped_date, self.website)
        elif reason == "Not implemented":
            raise NotImplementedError
        # else:
        #     print(f"Spider {self.name} closed")
        # TODO rethrow?


class SitemapWithCookiesSpider(SitemapSpider):
    def _parse_sitemap(self, response):
        if response.url.endswith('/robots.txt'):
            for url in sitemap_urls_from_robots(response.text, base_url=response.url):
                onet_cookies = get_onet_cookies()
                yield Request(url, callback=self._parse_sitemap, cookies=onet_cookies)
        else:
            body = self._get_sitemap_body(response)
            if body is None:
                logger.warning("Ignoring invalid sitemap: %(response)s",
                               {'response': response}, extra={'spider': self})
                return

            s = Sitemap(body)
            it = self.sitemap_filter(s)

            if s.type == 'sitemapindex':
                for loc in iterloc(it, self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        onet_cookies = get_onet_cookies()
                        yield Request(loc, callback=self._parse_sitemap, cookies=onet_cookies)
            elif s.type == 'urlset':
                for loc in iterloc(it, self.sitemap_alternate_links):
                    for r, c in self._cbs:
                        if r.search(loc):
                            onet_cookies = get_onet_cookies()
                            yield Request(loc, callback=c, cookies=onet_cookies)
                            break
