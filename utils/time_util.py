from datetime import *
from pytz import timezone
import json
from pathlib import Path
from json.decoder import JSONDecodeError

date_formats = {
    "fakt": "%Y-%m-%dT%H:%M:%S.%f%z",
    "onet": "%Y-%m-%d %H:%M:%S%z",
    "radiozet": "%d.%m.%Y %H:%M",
    "rmf24": "%Y-%m-%dT%H:%M:%S",
    # "tvn24": "%Y-%m-%dT%H:%M:%S.%f%z"
    "tvn24": "%Y-%m-%dT%H:%M:%S.%f"
}


def try_strptime(str, format):
    """
    @param str the string to parse
    @param format the format to attempt parsing of the given string
    @return the parsed datetime or None on failure to parse
    @see datetime.datetime.strptime
    """
    try:
        dt = datetime.strptime(str, format)
    except ValueError:
        dt = None
    return dt


def string_to_datetime(date_string: str, website: str) -> datetime:
    local = timezone("Poland")
    date_string = date_string.replace("Z", "+0000")
    dt = try_strptime(date_string, date_formats[website])
    if dt is not None and dt.tzinfo is None:
        dt = local.localize(dt)
    return dt


default_dates = {
    "fakt": "1900-01-01T00:00:00+00:00",
    "onet": "1900-01-01T00:00:00+00:00",
    "radiozet": "1900-01-01T00:00:00+00:00",
    "rmf24": "1900-01-01T00:00:00+00:00",
    "tvn24": "1900-01-01T00:00:00+00:00"
}
dates_path = Path('last_article_dates.json')


def create_last_scraped_dates():
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
