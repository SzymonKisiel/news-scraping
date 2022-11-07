from settings.onet_cookies import get_onet_cookies


def update_cookies():
    cookies = get_onet_cookies(True)
    for key in cookies.keys():
        print(f"{key}: {cookies[key]}")
