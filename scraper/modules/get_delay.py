from settings import delay_settings


def get_delay(website: str):
    return delay_settings.get_delay(website=website)
