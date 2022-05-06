import datetime

import scrapy
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from time import sleep
# from scrapy.crawler import CrawlRunner
# from scrapy.utils.log import configure_logging

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from Scraping2.spiders.fakt_spider import FaktNewsSpider
from Scraping2.spiders.onet_spider import OnetNewsSpider
from Scraping2.spiders.radiozet_spider import RadiozetNewsSpider
from Scraping2.spiders.rmf24_spider import Rmf24NewsSpider
from Scraping2.spiders.tvn24_spider import Tvn24NewsSpider

from utils import time_util

from datetime import timezone

websites = ['fakt', 'onet', 'radiozet', 'rmf24', 'tvn24']


def get_delay_name(crawler):
    if crawler == FaktNewsSpider:
        return "DELAY_FAKT"
    if crawler == Rmf24NewsSpider:
        return "DELAY_RMF24"



def my_task(test=0):
    print(f"starting task {test}...", end='')
    sleep(1)
    print(f"ending task {test}")


def crawl_job(settings: scrapy.crawler.Settings, crawler):
    """
    Job to start spiders.
    Return Deferred, which will execute after crawl has completed.
    """
    runner = CrawlerRunner(settings)
    return runner.crawl(crawler)


def schedule_next_crawl(null, sleep_time, crawler):
    """
    Schedule the next crawl
    """
    reactor.callLater(sleep_time, crawl, crawler)


def crawl(crawler):
    """
    A "recursive" function that schedules a crawl 30 seconds after
    each successful crawl.
    """
    settings = get_project_settings()
    # save all scraped data without checking duplicates
    settings.set("FEEDS", {
        "data/test_items.jsonl": {"format": "jsonlines", "encoding": "utf8"},
    })
    # crawl_job() returns a Deferred
    d = crawl_job(settings, crawler)

    delay = settings.get(crawler.delay_setting_name)
    # call schedule_next_crawl(<scrapy response>, n) after crawl job is complete
    d.addCallback(schedule_next_crawl, delay, crawler)
    d.addErrback(catch_error)


def catch_error(failure):
    print(failure)


def main():
    # crawl(Rmf24NewsSpider)
    # crawl(RadiozetNewsSpider)
    # reactor.run()
    dt = datetime.datetime.now(timezone.utc).astimezone()
    print(dt)
    print(dt.isoformat())
    print(datetime.datetime.fromisoformat(dt.isoformat()))
    time_util.set_last_scraped_date(dt, "rmf24")


if __name__ == '__main__':
    main()
