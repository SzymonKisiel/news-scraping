from utils.time_util import set_last_scraped_date
from utils.websites_util import websites
import pytz
from datetime import *


def set_scraping_start(end_date: str, website: str):
    if end_date == 'now':
        dt = datetime.now()
    else:
        dt = datetime.fromisoformat(end_date)

    local = pytz.timezone("Poland")
    if dt.tzinfo is None:
        dt = local.localize(dt)

    set_last_scraped_date(dt, website)
