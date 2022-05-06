import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Scraping2.spiders.fakt_spider import FaktNewsSpider
from Scraping2.spiders.onet_spider import OnetNewsSpider
from Scraping2.spiders.radiozet_spider import RadiozetNewsSpider
from Scraping2.spiders.rmf24_spider import Rmf24NewsSpider
from Scraping2.spiders.tvn24_spider import Tvn24NewsSpider


def crawl(name: str):
    settings = get_project_settings()
    # save all scraped data without checking duplicates
    settings.set("FEEDS", {
        "data/items.jsonl": {"format": "jsonlines", "encoding": "utf8"},
    })

    process = CrawlerProcess(settings)
    if name == 'fakt':
        process.crawl(FaktNewsSpider)
    elif name == 'onet':
        process.crawl(OnetNewsSpider)
    elif name == 'radiozet':
        process.crawl(RadiozetNewsSpider)
    elif name == 'rmf24':
        process.crawl(Rmf24NewsSpider)
    elif name == 'tvn24':
        process.crawl(Tvn24NewsSpider)

    process.start()  # the script will block here until the crawling is finished
