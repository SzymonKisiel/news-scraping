import os


def get_production():
    return os.environ.get("PRODUCTION")


def get_scraper_api():
    return os.environ.get("SCRAPER_API")
