import datetime
from utils.time_util import string_to_datetime, get_timezone_aware_now
from twisted.internet import defer
from scrapy.crawler import CrawlerProcess
from reactor_queue import ReactorQueue
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from Scraping2.spiders.test_spider1 import AuthorSpider
from Scraping2.spiders.test_spider2 import QuotesSpider
from scrapy.settings import Settings
from scrapy import Spider
from utils.websites_util import website_name_to_crawler


@defer.inlineCallbacks
def run(spider: Spider,
        queue: ReactorQueue,
        settings: Settings,
        delay: int = 60,
        crawl_count: int = None,
        due_time: datetime = None,
        i: int = 0):

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
        reactor.callLater(delay, run, spider, queue, settings, delay, crawl_count, due_time, i + 1)

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


def crawl_websites(websites: list[str], due_time: str = None, crawl_count: int = None):
    queue = ReactorQueue(len(websites))
    for website in websites:
        # get settings
        settings = get_project_settings()
        settings.set("FEEDS", {
            f"data/test66/{website}.jsonl": {"format": "jsonlines", "encoding": "utf8"},
        })
        settings.set("LOG_ENABLED", False)

        crawler = website_name_to_crawler(website)
        if crawler is None:
            raise Exception(f"Website \"{website}\" does not exist")

        delay = settings.get(crawler.delay_setting_name)

        # run
        run_wrapper(crawler, queue, settings, delay)
        # run(crawler, queue, settings, delay, due_time=due_time, crawl_count=crawl_count)
    reactor.run()

