from settings.last_article_dates import set_last_scraped_date
from datetime import *
from utils.time_util import string_to_datetime, get_timezone_aware_now


def set_scraping_start(end_date: str, website: str):
    if end_date == 'now':
        dt = get_timezone_aware_now()
    else:
        dt = string_to_datetime(end_date)
    set_last_scraped_date(dt, website)
