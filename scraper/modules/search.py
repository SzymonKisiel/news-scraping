# import json
import re
import pandas as pd
from pathlib import Path
from utils.websites_util import website_name_to_data_filename
from utils.websites_util import websites

path_to_file = '../data/items.jsonl'
data_paths = {
    "fakt": "1900-01-01T00:00:00+00:00",
    "onet": "1900-01-01T00:00:00+00:00",
    "radiozet": "1900-01-01T00:00:00+00:00",
    "rmf24": "1900-01-01T00:00:00+00:00",
    "tvn24": "1900-01-01T00:00:00+00:00"
}

data_dir = Path('data')


def search(word: str, path: Path):
    path_string = path.as_posix()
    if not path.is_file():
        print(f'The file {path_string} does not exist')
        return

    dataframe = pd.read_json(path_or_buf=path_string, lines=True)
    data = dataframe.to_dict('records')

    for i in data:
        for j in i.items():
            if j[1] is None:
                continue
            z = [m.start() for m in re.finditer(str(word), str(j[1]))]  # should use regex?
            if len(z) > 0:
                print(f"Found word \"{word}\" in {j[0]} at indices {z} at url {i['url']}")


def search_websites(word: str):
    for website in websites:
        path = Path(data_dir, website_name_to_data_filename(website))
        search(word, path)
