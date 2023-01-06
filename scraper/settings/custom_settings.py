import os
from typing import Dict

from scrapy.settings import Settings
from utils.websites_util import website_name_to_data_filename


def get_project_settings():
    settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'news_scraping.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='project')
    return settings


def get_custom_project_settings(website: str, flags: Dict):
    if flags is not None:
        save_to_json = flags.get('save_to_json', False)
        save_to_database = flags.get('save_to_database', True)

    settings = get_project_settings()
    if save_to_json and website is not None:
        filename = website_name_to_data_filename(website)
        settings.set("FEEDS", {
            f"data/{filename}": {"format": "jsonlines", "encoding": "utf8"},
        })
    if save_to_database:
        settings.set("ITEM_PIPELINES", {
            'news_scraping.pipelines.ArticlesPipeline': 300
        })
    settings.set("LOG_ENABLED", False)
    # settings.set("COOKIES_DEBUG", True)

    return settings
