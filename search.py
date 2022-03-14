# import json
import re
import pandas as pd


def search(word: str):
    # f = open('items.jsonl', encoding="utf8")
    # data = json.load(f)
    dataframe = pd.read_json(path_or_buf='data/items.jsonl', lines=True)
    data = dataframe.to_dict('records')

    for i in data:
        for j in i.items():
            z = [m.start() for m in re.finditer(word, j[1])]  # should use regex?
            if len(z) > 0:
                print(f"Found word \"{word}\" in {j[0]} at indices {z} at url {i['url']}")
