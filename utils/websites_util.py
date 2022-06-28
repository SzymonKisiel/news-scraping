from Scraping2.spiders.fakt_spider import FaktNewsSpider
from Scraping2.spiders.onet_spider import OnetNewsSpider
from Scraping2.spiders.radiozet_spider import RadiozetNewsSpider
from Scraping2.spiders.rmf24_spider import Rmf24NewsSpider
from Scraping2.spiders.tvn24_spider import Tvn24NewsSpider
from scrapy import Spider

websites = ['fakt', 'onet', 'radiozet', 'rmf24', 'tvn24']
websites_name_crawler = {
    'fakt': FaktNewsSpider,
    'onet': OnetNewsSpider,
    'radiozet': RadiozetNewsSpider,
    'rmf24': Rmf24NewsSpider,
    'tvn24': Tvn24NewsSpider
}


def website_name_to_crawler(website_name: str):
    """
    Returns website Spider for website name
    Returns None if website name is incorrect
    """
    if website_name not in websites:
        return None
    return websites_name_crawler[website_name]
