# import json
import re
import pandas as pd
from pathlib import Path

path_to_file = 'data/items.jsonl'


def search(word: str):
    # f = open('items.jsonl', encoding="utf8")
    # data = json.load(f)

    path = Path(path_to_file)
    if not path.is_file():
        print(f'The file {path_to_file} does not exist')
        return

    dataframe = pd.read_json(path_or_buf=path_to_file, lines=True)
    data = dataframe.to_dict('records')

    for i in data:
        for j in i.items():
            if j[1] is None:
                continue
            z = [m.start() for m in re.finditer(word, j[1])]  # should use regex?
            if len(z) > 0:
                print(f"Found word \"{word}\" in {j[0]} at indices {z} at url {i['url']}")
