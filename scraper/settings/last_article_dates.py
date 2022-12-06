from pathlib import Path
from datetime import datetime
import json
from json.decoder import JSONDecodeError

default_dates = {
    "fakt": "1900-01-01T00:00:00+00:00",
    "onet": "1900-01-01T00:00:00+00:00",
    "radiozet": "1900-01-01T00:00:00+00:00",
    "rmf24": "1900-01-01T00:00:00+00:00",
    "tvn24": "1900-01-01T00:00:00+00:00"
}

dates_path_dir = Path('data/settings')
dates_path = Path(dates_path_dir, 'last_article_dates.json')


def create_last_scraped_dates():
    if not dates_path_dir.exists():
        dates_path_dir.mkdir(parents=True, exist_ok=True)
    dates_path.touch(exist_ok=True)
    with open(dates_path, 'w') as file:
        json.dump(default_dates, file)


def get_last_scraped_date(website: str) -> datetime:
    if not dates_path.is_file():
        create_last_scraped_dates()
    with open(dates_path, 'r') as f:
        try:
            last_scraped_dates = json.load(f)
        except JSONDecodeError:
            last_scraped_dates = default_dates

    dt = datetime.fromisoformat(last_scraped_dates[website])
    return dt


def set_last_scraped_date(dt: datetime, website: str):
    if not dates_path.is_file():
        create_last_scraped_dates()
    with open(dates_path, 'r') as file:
        try:
            last_scraped_dates = json.load(file)
        except JSONDecodeError:
            last_scraped_dates = default_dates
        if website not in last_scraped_dates:
            raise KeyError("website is not available")
    last_scraped_dates[website] = dt.isoformat()
    with open(dates_path, 'w') as file:
        json.dump(last_scraped_dates, file)
