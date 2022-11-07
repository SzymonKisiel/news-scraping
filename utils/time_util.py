from datetime import datetime
from pytz import timezone, utc
from utils.websites_util import date_formats


DEFAULT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def try_strptime(date_string: str, date_format):
    """
    @param date_string the string to parse
    @param date_format the format to attempt parsing of the given string
    @return the parsed datetime or None on failure to parse
    @see datetime.datetime.strptime
    """
    try:
        dt = datetime.strptime(date_string, date_format)
    except ValueError:
        dt = None
    return dt


def string_to_datetime(date_string: str, website: str = None) -> datetime:
    """A dummy docstring."""
    local = timezone("Poland")
    date_string = date_string.replace("Z", "+0000")
    if website is not None:
        date_format = date_formats[website]
    else:
        date_format = DEFAULT_DATE_FORMAT
    dt = try_strptime(date_string, date_format)
    if dt is not None and dt.tzinfo is None:
        dt = local.localize(dt)
    return dt


def get_timezone_aware_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=utc)
