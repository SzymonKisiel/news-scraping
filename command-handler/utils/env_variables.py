import os


def get_production():
    return os.environ.get("PRODUCTION")


def get_scraper_api():
    return os.environ.get("SCRAPER_API")


def get_sentiment_analyser_api():
    return os.environ.get("SENTIMENT_ANALYSER_API")
