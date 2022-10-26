from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json
from json.decoder import JSONDecodeError


cookies_path_dir = Path('data/settings')
cookies_path = Path(cookies_path_dir, 'onet_cookies.json')


def renew_onet_cookies():
    print('test')

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("window-size=1400,2100")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.onet.pl")

    accept_cookies_btn_selector = ".cmp-intro_acceptAll > span"
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, accept_cookies_btn_selector)))
    button.click()
    cookies = driver.get_cookies()

    cookies_dict = {}
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']

    driver.quit()

    return cookies_dict


def renew_onet_cookies_file():
    with open(cookies_path, 'w') as file:
        cookies = renew_onet_cookies()
        json.dump(cookies, file)
        return cookies


def create_onet_cookies_file():
    if not cookies_path_dir.exists():
        cookies_path_dir.mkdir(parents=True, exist_ok=True)
    cookies_path.touch(exist_ok=True)
    renew_onet_cookies_file()


def get_onet_cookies(renew_cookies=False):
    if not cookies_path.is_file() or renew_cookies:
        create_onet_cookies_file()
    with open(cookies_path, 'r') as f:
        try:
            cookies = json.load(f)
        except JSONDecodeError:
            cookies = renew_onet_cookies_file()
    return cookies
