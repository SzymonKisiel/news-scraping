import datetime
from scrapy.utils.project import get_project_settings
from twisted.internet import defer
from scrapy.crawler import CrawlerProcess
from scrapy import Spider
from twisted.internet import reactor
from news_scraping.spiders.test_spider1 import AuthorSpider
from news_scraping.spiders.test_spider2 import QuotesSpider
from scrapy.settings import Settings
from utils.reactor_queue import ReactorQueue
from utils.time_util import get_timezone_aware_now


def test():
    print("Test started")

    websites = ['authors', 'quotes']

    settings = get_project_settings()
    settings.set("FEEDS", {
        f"data/test_test/authors.jsonl": {"format": "jsonlines", "encoding": "utf8"},
    })
    settings.set("LOG_ENABLED", False)

    settings2 = get_project_settings()
    settings2.set("FEEDS", {
        f"data/test_test/quotes.jsonl": {"format": "jsonlines", "encoding": "utf8"},
    })
    settings2.set("LOG_ENABLED", False)

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
    # due_time1 = string_to_datetime("2022-10-14T18:00:00+0200")
    # due_time2 = string_to_datetime("2022-10-14T17:50:00+0200")
    # run_wrapper3(AuthorSpider, queue, settings, 20, due_time1)
    # run_wrapper3(QuotesSpider, queue, settings2, 30, due_time2)

    reactor.run()

    print("Test finished")


# @defer.inlineCallbacks
# def run(spider: Spider,
#         queue: ReactorQueue,
#         settings: Settings,
#         delay: int = 60,
#         i: int = 0,
#         crawl_count: int = None,
#         due_time: datetime = None):
#     print(f"[{datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] {spider.name} run {i}")
#
#     runner = CrawlerProcess(settings)
#     yield runner.crawl(spider)
#
#     now = get_timezone_aware_now()
#     now_delayed = now + datetime.timedelta(seconds=delay)
#     reached_due_time = now_delayed > due_time if due_time is not None else False
#     reached_max_count = i + 1 >= crawl_count if crawl_count is not None else False
#
#     if not reached_due_time and not reached_max_count:
#         reactor.callLater(delay, run, spider, queue, settings, delay, i + 1, crawl_count, due_time)
#     else:
#         queue.pop()


@defer.inlineCallbacks
def run(spider: Spider,
        queue: ReactorQueue,
        settings: Settings,
        delay: int = 60,
        i: int = 0,
        crawl_count: int = None,
        due_time: datetime = None):

    # check conditions
    if due_time is not None:
        now_delayed = get_timezone_aware_now() + datetime.timedelta(seconds=delay)
        reached_due_time = now_delayed > due_time
    else:
        reached_due_time = False

    if crawl_count is not None:
        reached_max_count = i + 1 >= crawl_count
    else:
        reached_max_count = False

    reached_any_end_condition = reached_due_time or reached_max_count

    # schedule next crawl
    if not reached_any_end_condition:
        reactor.callLater(delay, run, spider, queue, settings, delay, i + 1, crawl_count, due_time)

    # log crawl start
    print(f"[{datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S.%f')}] {spider.name} run {i}")

    # run crawler
    runner = CrawlerProcess(settings)
    yield runner.crawl(spider)

    # pop runners queue if crawler ends
    if reached_any_end_condition:
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
