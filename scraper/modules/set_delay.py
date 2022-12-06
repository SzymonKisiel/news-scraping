from settings import delay_settings


def set_delay(website: str, delay: int):
    delay_settings.set_delay(website=website, delay=delay)
