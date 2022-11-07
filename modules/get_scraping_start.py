from settings.last_article_dates import get_last_scraped_date


def get_scraping_start(website: str):
    return get_last_scraped_date(website)
