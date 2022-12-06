import logging

from modules.crawl import async_crawl_websites
from modules.set_scraping_start import set_scraping_start
from modules.get_scraping_start import get_scraping_start
from modules.set_delay import set_delay
from modules.get_delay import get_delay
from utils.websites_util import websites
from flask_server.models import *


class ScraperService:
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def crawl(self, request: CrawlRequest):
        self.logger.debug("crawl")
        async_crawl_websites(
            request.websites,
            due_time=request.due_time,
            run_time=request.run_time,
            crawls_amount=request.crawls_amount)

    def get_delay(self, request: GetDelayRequest):
        self.logger.debug("get_delay")
        result = {}
        for website in request.websites:
            result[website] = get_delay(website)
        return result

    def get_scraping_start(self, request: GetScrapingStartRequest):
        self.logger.debug("get_scraping_start")
        result = {}
        for website in request.websites:
            result[website] = get_scraping_start(website).isoformat()
        return result

    def get_websites(self):
        self.logger.debug("get_websites")
        return websites

    def set_delay(self, request: SetDelayRequest):
        self.logger.debug("set_delay")
        for website in request.websites:
            set_delay(website, request.delay)

    def set_scraping_start(self, request: SetScrapingStartRequest):
        self.logger.debug("set_scraping_start")
        for website in request.websites:
            set_scraping_start(request.date, website)
