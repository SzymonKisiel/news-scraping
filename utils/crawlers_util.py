from utils.websites_util import websites
from news_scraping.spiders.fakt_spider import FaktNewsSpider
from news_scraping.spiders.onet_spider import OnetNewsSpider
from news_scraping.spiders.radiozet_spider import RadiozetNewsSpider
from news_scraping.spiders.rmf24_spider import Rmf24NewsSpider
from news_scraping.spiders.tvn24_spider import Tvn24NewsSpider
from news_scraping.spiders.test_spider1 import AuthorSpider
from news_scraping.spiders.test_spider2 import QuotesSpider


websites_name_crawler = {
    'fakt': FaktNewsSpider,
    'onet': OnetNewsSpider,
    'radiozet': RadiozetNewsSpider,
    'rmf24': Rmf24NewsSpider,
    'tvn24': Tvn24NewsSpider,
    'test1': AuthorSpider,
    'test2': QuotesSpider
}


def website_name_to_crawler(website_name: str):
    """
    Returns website Spider for website name
    Returns None if website name is incorrect
    """
    if website_name not in websites:
        return None
    return websites_name_crawler[website_name]