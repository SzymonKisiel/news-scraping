websites = [
    'fakt', 'onet', 'radiozet', 'rmf24', 'tvn24',
    # 'test1', 'test2'
]

date_formats = {
    "fakt": "%Y-%m-%dT%H:%M:%S.%f%z",
    "onet": "%Y-%m-%d %H:%M:%S%z",
    "radiozet": "%d.%m.%Y %H:%M",
    "rmf24": "%Y-%m-%dT%H:%M:%S",
    "tvn24": "%Y-%m-%dT%H:%M:%S.%f"
}


def website_name_to_data_filename(website_name: str) -> str:
    return website_name + ".jsonl"
