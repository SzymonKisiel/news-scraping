import logging

from services.scraper_service import ScraperService
from services.search_service import SearchService
from services.models import *

from app import create_app

from dotenv import load_dotenv


# def start_client():
#     # host = sys.argv[1]
#     print(f"{SERVER_HOST}:{SERVER_PORT}")
#     server = TestClient(SERVER_HOST, SERVER_PORT)
#     server.open_conncetion()
#     server.test_connection()
#     # server.test_connection()
#     server.close_connection()


# def test_scraper():
#     # requests.get('http://localhost:5000/api/scraper/get-delay')
#     logger = logging.getLogger('command_handler')
#     service = ScraperService(logger)
#
#     data = {
#         "websites": [
#             "rmf24",
#             "onet",
#             "fakt"
#         ]
#     }
#     req = GetDelayRequest(**data)
#
#     delays = service.get_delay(req)
#     print(delays)


# def test_scraper():
#     logger = logging.getLogger('command_handler')
#     service = ScraperService(logger)


def test_search():
    logger = logging.getLogger('command_handler')
    logger.setLevel(logging.DEBUG)
    service = SearchService(logger)
    articles = service.get_all_articles()
    article = service.get_article_by_id(1612)


def start_flask():
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     logging.basicConfig()
#     start_flask()

load_dotenv()
from utils.env_variables import get_production, get_scraper_api
print(f"Is production: {get_production()}")
print(f"Scraper api: {get_scraper_api()}")

logging.basicConfig()
app = create_app()

if __name__ == '__main__':
    # development - local configuration
    app.run(host='0.0.0.0', port=5001, debug=True)
else:
    # production - gunicorn configuration
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

