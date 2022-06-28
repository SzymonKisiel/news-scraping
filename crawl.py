from sys import stdin
from twisted.internet import reactor

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

from multiprocessing import Process, Queue

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from utils.websites_util import website_name_to_crawler


# Enable logging for CrawlerRunner
# configure_logging()

def startup_message():
    print("STARTING REACTOR...")


def shutdown_message():
    print("STOPPING REACTOR...")


class CrawlerRunnerProcess(Process):
    def __init__(self, spider, *args):
        Process.__init__(self)
        settings = get_project_settings()
        settings.set("FEEDS", {
            f"data/test2/{spider.website}.jsonl": {"format": "jsonlines", "encoding": "utf8"},
        })
        self.runner = CrawlerRunner(settings)
        self.spider = spider
        self.args = args

    def run(self):
        deferred = self.runner.crawl(self.spider, self.args)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run(installSignalHandlers=False)


# The wrapper to make it run multiple spiders, multiple times
def run_spider(spider, *args):
    runner = CrawlerRunnerProcess(spider, *args)
    runner.start()
    runner.join()


def crawl(website_name):
    settings = get_project_settings()
    settings.set("FEEDS", {
        f"data/test2/{website_name}.jsonl": {"format": "jsonlines", "encoding": "utf8"},
    })

    crawler = website_name_to_crawler(website_name)
    if crawler is None:
        raise Exception(f"Website \"{website_name}\" does not exist")
    delay = settings.get(crawler.delay_setting_name)

    print("debug")
    print(f"Debug:\ndelay_setting_name = {crawler.delay_setting_name}\ndelay = {delay}")
    delay = 100

    deferred = task.LoopingCall(reactor.callLater, 0, run_spider, crawler)
    deferred.start(delay)


# async def cmdloop():
#     while True:
#         print("loop")
#         line = ''
#         # line = stdin.readline()
#         line = await aioconsole.ainput('Is this your line?')
#         if line == "stop":
#             break
#         sleep(3)
#     if reactor.running:
#         print("Received stop signal")
#         reactor.stop()


def crawl_websites(websites: list[str]):
    # websites = [
    #     "fakt",
    #     "rmf24",
    #     "onet",
    #     "radiozet",
    #     "tvn24"
    # ]
    if reactor.running:
        reactor.stop()

    for website in websites:
        crawl(website)

    reactor.addSystemEventTrigger('during', 'startup', startup_message)
    reactor.addSystemEventTrigger('during', 'shutdown', shutdown_message)
    # reactor.callInThread(cmdloop)
    # reactor.run()
