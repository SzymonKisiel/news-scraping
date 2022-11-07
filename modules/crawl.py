import datetime
from utils.time_util import string_to_datetime, get_timezone_aware_now
from twisted.internet import defer
from scrapy.crawler import CrawlerProcess
from utils.reactor_queue import ReactorQueue
from twisted.internet import reactor
from scrapy.settings import Settings
from scrapy import Spider
from utils.crawlers_util import website_name_to_crawler
from settings.delay_settings import get_delay
from settings.custom_settings import get_custom_project_settings


@defer.inlineCallbacks
def run(spider: Spider,
        queue: ReactorQueue,
        settings: Settings,
        delay: int = 60,
        crawls_amount: int = None,
        due_time: datetime = None,
        i: int = 0):

    # check conditions
    if due_time is not None:
        now_delayed = get_timezone_aware_now() + datetime.timedelta(seconds=delay)
        reached_due_time = now_delayed > due_time
    else:
        reached_due_time = False

    if crawls_amount is not None:
        reached_max_count = i + 1 >= crawls_amount
    else:
        reached_max_count = False

    reached_any_end_condition = reached_due_time or reached_max_count

    # schedule next crawl
    if not reached_any_end_condition:
        reactor.callLater(delay, run, spider, queue, settings, delay, crawls_amount, due_time, i + 1)

    # log crawl start
    print(f"[{datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S.%f')}] {spider.name} run {i}")

    # run crawler
    runner = CrawlerProcess(settings)
    yield runner.crawl(spider)

    # pop runners queue if crawler ends
    if reached_any_end_condition:
        queue.pop()


# convert due_time from string to datetime and choose the earliest due time from due_time and run_time
def run_wrapper(spider: Spider, queue: ReactorQueue, settings: Settings, delay: int, due_time: str, run_time: int,
                crawls_amount: int):
    due_time_dt = None
    if due_time is not None:
        due_time_dt = string_to_datetime(due_time)
    if run_time is not None:
        run_time_dt = get_timezone_aware_now() + datetime.timedelta(seconds=run_time)
        if due_time_dt is None or run_time_dt < due_time_dt:
            due_time_dt = run_time_dt

    run(spider, queue, settings, delay, due_time=due_time_dt, crawls_amount=crawls_amount)


def crawl_websites(websites: list[str], due_time: str = None, run_time: int = None, crawls_amount: int = None):
    queue = ReactorQueue(len(websites))
    for website in websites:
        crawler = website_name_to_crawler(website)
        if crawler is None:
            raise Exception(f"Website \"{website}\" does not exist")
        settings = get_custom_project_settings(website)
        delay = get_delay(website)

        run_wrapper(crawler, queue, settings, delay, due_time=due_time, run_time=run_time, crawls_amount=crawls_amount)
    reactor.run()

