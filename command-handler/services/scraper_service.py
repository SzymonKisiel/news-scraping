import logging
import requests
from services.models import *
from utils.env_variables import get_scraper_api


class ScraperService:
    logger: logging.Logger
    host: str

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.host = 'localhost'
        # self.host = 'scraper'
        self.api_url = f'http://{self.host}:5002/api/scraper/'
        self.api_url = get_scraper_api()

    def crawl(self, request: CrawlRequest):
        self.logger.debug('crawl')

        action = '/crawl'
        url = self.api_url + action

        request_dict = request.dict()

        response = requests.post(url, json=request_dict)
        return response

    def get_delay(self, request: GetDelayRequest):
        self.logger.debug('get_delay')

        action = '/get-delay'
        url = self.api_url + action
        request_dict = request.dict()

        response = requests.post(url, json=request_dict)
        return response.json()

    def get_scraping_start(self, request: GetScrapingStartRequest):
        self.logger.debug('get_scraping_start')

        action = '/get-scraping-start'
        url = self.api_url + action
        request_dict = request.dict()

        response = requests.post(url, json=request_dict)
        return response.json()

    def get_websites(self):
        self.logger.debug('get_websites')

        action = '/get-websites'
        url = self.api_url + action

        response = requests.get(url)
        return response.json()

    def set_delay(self, request: SetDelayRequest):
        self.logger.debug('set_delay')

        action = '/set-delay'
        url = self.api_url + action
        request_dict = request.dict()

        response = requests.post(url, json=request_dict)
        return response.json()

    def set_scraping_start(self, request: SetScrapingStartRequest):
        self.logger.debug('set_scraping_start')

        action = '/set-scraping-start'
        url = self.api_url + action
        request_dict = request.dict()

        response = requests.post(url, json=request_dict)
        return response.json()
