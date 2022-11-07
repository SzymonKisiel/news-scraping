from scrapy.utils.project import get_project_settings
from utils.websites_util import website_name_to_data_filename


def get_custom_project_settings(website: str):
    settings = get_project_settings()
    if website is not None:
        filename = website_name_to_data_filename(website)
        settings.set("FEEDS", {
            f"data/{filename}": {"format": "jsonlines", "encoding": "utf8"},
        })
    settings.set("LOG_ENABLED", False)
    return settings
