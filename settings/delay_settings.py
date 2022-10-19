from pathlib import Path
import json
from json.decoder import JSONDecodeError


default_delay_settings = {
    "fakt": 3600,
    "onet": 3600,
    "radiozet": 3600,
    "rmf24": 3600,
    "tvn24": 3600
}

delay_settings_path_dir = Path('data/settings')
delay_settings_path = Path(delay_settings_path_dir, 'delay_settings.json')


def create_delay_settings():
    if not delay_settings_path_dir.exists():
        delay_settings_path_dir.mkdir(parents=True, exist_ok=True)
    delay_settings_path.touch(exist_ok=True)
    with open(delay_settings_path, 'w') as file:
        json.dump(default_delay_settings, file)


def get_delay(website: str) -> int:
    if not delay_settings_path.is_file():
        create_delay_settings()
    with open(delay_settings_path, 'r') as f:
        try:
            delay_settings = json.load(f)
        except JSONDecodeError:
            delay_settings = default_delay_settings

    delay = delay_settings[website]
    return delay


def set_delay(delay: int, website: str):
    if not delay_settings_path.is_file():
        create_delay_settings()
    with open(delay_settings_path, 'r') as file:
        try:
            delay_settings = json.load(file)
        except JSONDecodeError:
            delay_settings = default_delay_settings
        if website not in delay_settings:
            raise KeyError("website is not available")
    delay_settings[website] = delay
    with open(delay_settings_path, 'w') as file:
        json.dump(delay_settings, file)


def get_all_delay_settings():
    if not delay_settings_path.is_file():
        create_delay_settings()
    with open(delay_settings_path, 'r') as f:
        try:
            delay_settings = json.load(f)
        except JSONDecodeError:
            delay_settings = delay_settings_path

    return delay_settings
