import os

from scrapy.settings import Settings
from utils.websites_util import website_name_to_data_filename


def get_project_settings():
    settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'news_scraping.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='project')
    return settings


def get_custom_project_settings(website: str):
    settings = get_project_settings()
    if website is not None:
        filename = website_name_to_data_filename(website)
        settings.set("FEEDS", {
            f"data/{filename}": {"format": "jsonlines", "encoding": "utf8"},
        })
    settings.set("LOG_ENABLED", False)
    # settings.set("COOKIES_DEBUG", True)

    return settings
