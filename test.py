import datetime
from itertools import count
from sys import stdin

import scrapy.settings
from twisted.internet import reactor

from utils.time_util import string_to_datetime, get_timezone_aware_now
from time import sleep
from twisted.internet import reactor, defer, task
import signal

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from Scraping2.spiders.fakt_spider import FaktNewsSpider
from Scraping2.spiders.onet_spider import OnetNewsSpider
from Scraping2.spiders.radiozet_spider import RadiozetNewsSpider
from Scraping2.spiders.rmf24_spider import Rmf24NewsSpider
from Scraping2.spiders.tvn24_spider import Tvn24NewsSpider
from scrapy.exceptions import CloseSpider

import logging
import pytz

from multiprocessing import Process, Queue
from reactor_queue import ReactorQueue

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from Scraping2.spiders.test_spider1 import AuthorSpider
from Scraping2.spiders.test_spider2 import QuotesSpider

from scrapy.settings import Settings
from scrapy import Spider


def test():
    print("Test started")

    websites = ['authors', 'quotes']
    crawl_count = 2
    # crawl_websites(websites)
    settings = get_project_settings()
    settings.set("FEEDS", {
        f"data/test_fajne/authors.jsonl": {"format": "jsonlines", "encoding": "utf8"},
    })
    settings.set("LOG_ENABLED", False)
    runner = CrawlerRunner(settings)

    settings2 = get_project_settings()
    settings2.set("FEEDS", {
        f"data/test_fajne/quotes.jsonl": {"format": "jsonlines", "encoding": "utf8"},
    })
    settings2.set("LOG_ENABLED", False)
    runner2 = CrawlerRunner(settings2)

    ###############################################
    # runner.crawl(AuthorSpider)
    # runner2.crawl(QuotesSpider)
    #
    # d = runner.join()
    # d.addCallback(30, run_spider)

    ###############################################
    # @defer.inlineCallbacks
    # def test_crawl(i=0):
    #     print(f"Test crawl {i}")
    #     yield runner.crawl(AuthorSpider)
    #     yield runner2.crawl(QuotesSpider)
    #     reactor.callLater(10, test_crawl, i + 1)
    #     reactor.stop()

    # test_crawl()
    # reactor.run()

    ###############################################
    # run_test1()
    # run_test2()
    # reactor.run()

    ###############################################
    queue = ReactorQueue(2)
    # run infinitely
    # run_wrapper(AuthorSpider, queue, settings, 4)
    # run_wrapper(QuotesSpider, queue, settings2, 6)

    # run n times
    run_wrapper2(AuthorSpider, queue, settings, 3, 1)
    run_wrapper2(QuotesSpider, queue, settings2, 2.5, 4)

    # run once
    # run_wrapper2(AuthorSpider, queue, settings, 0, 1)
    # run_wrapper2(QuotesSpider, queue, settings2, 0, 1)

    # run for x time
    # due_time1 = datetime.datetime.now() + datetime.timedelta(seconds=18)
    # due_time2 = datetime.datetime.now() + datetime.timedelta(seconds=10)
    # run_wrapper3(AuthorSpider, queue, settings, 4, due_time1)
    # run_wrapper3(QuotesSpider, queue, settings2, 6, due_time2)

    # run to due time
    # due_time1 = string_to_datetime("2022-10-13T16:52:00+0200")
    # due_time2 = string_to_datetime("2022-10-13T16:54:00+0200")
    # run_wrapper3(AuthorSpider, queue, settings, 20, due_time1)
    # run_wrapper3(QuotesSpider, queue, settings2, 30, due_time2)

    reactor.run()

    print("Test finished")


# def run_test1(i=0):
#     print(f"[{datetime.datetime.now()}] Test1 run {i}")

#     settings = get_project_settings()
#     settings.set("FEEDS", {
#         f"data/test_fajne/authors.jsonl": {"format": "jsonlines", "encoding": "utf8"},
#     })
#     settings.set("LOG_ENABLED", False)
#     runner = CrawlerProcess(settings)
#     runner.crawl(AuthorSpider)

#     reactor.callLater(10, run_test1, i + 1)


# def run_test2(i=0):
#     print(f"[{datetime.datetime.now()}] Test2 run {i}")

#     settings = get_project_settings()
#     settings.set("FEEDS", {
#         f"data/test_fajne/quotes.jsonl": {"format": "jsonlines", "encoding": "utf8"},
#     })
#     settings.set("LOG_ENABLED", False)
#     runner = CrawlerProcess(settings)
#     runner.crawl(QuotesSpider)
#     reactor.callLater(20, run_test2, i + 1)


@defer.inlineCallbacks
def run(spider: Spider,
        queue: ReactorQueue,
        settings: Settings,
        delay: int = 60,
        i: int = 0,
        crawl_count: int = None,
        due_time: datetime = None):
    print(f"[{datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {spider.name} run {i}")

    runner = CrawlerProcess(settings)
    yield runner.crawl(spider)

    now = get_timezone_aware_now()
    now_delayed = now + datetime.timedelta(seconds=delay)
    reached_due_time = now_delayed > due_time if due_time is not None else False
    reached_max_count = i + 1 >= crawl_count if crawl_count is not None else False

    if not reached_due_time and not reached_max_count:
        reactor.callLater(delay, run, spider, queue, settings, delay, i + 1, crawl_count, due_time)
    else:
        queue.pop()


# run infinitely
def run_wrapper(spider, queue, settings, delay):
    run(spider, queue, settings, delay)


# run n times
def run_wrapper2(spider: Spider, queue: ReactorQueue, settings: Settings, delay: int, crawl_count: int):
    run(spider, queue, settings, delay, crawl_count=crawl_count)


# run to due time
def run_wrapper3(spider, queue, settings, delay, due_time):
    run(spider, queue, settings, delay, due_time=due_time)


# run for x seconds
def run_wrapper4(spider, queue, settings, delay, run_time):
    due_time = datetime.datetime.now() + datetime.timedelta(seconds=run_time)
    run(spider, queue, settings, delay, due_time=due_time)

