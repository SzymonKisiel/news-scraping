import logging
from flask import Flask, request, make_response, jsonify, Blueprint
from flask_cors import CORS
from pydantic import ValidationError
from services.search_service import SearchService
from services.scraper_service import ScraperService
from services.models import *

bp = Blueprint('route_prefix', __name__, template_folder='templates', url_prefix='/api/command-handler')

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

logger = logging.getLogger('gunicorn.error')
app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

scraper_service = ScraperService(app.logger)
search_service = SearchService(app.logger)


@bp.route('/')
def hello():
    return 'Command handler service'


@bp.route('crawl', methods=['POST'])
def crawl():
    try:
        req = request.get_json()
        request_dto = CrawlRequest(**req)
    except ValidationError as e:
        print(e.json())
        return make_response("Validation error", 400)

    scraper_service.crawl(request_dto)

    ok_response = {'message': 'Crawl started', 'code': 200}
    return jsonify(ok_response), 200


@bp.route('get-delay', methods=['POST'])
def get_delay():
    try:
        req = GetDelayRequest(**request.get_json())
    except ValidationError as e:
        response = {
            'code': 400,
            'message': 'Validation error',
            'detail': e.errors()
        }
        app.logger.debug(response)
        return make_response(jsonify(response), 400)

    response = scraper_service.get_delay(req)
    response_code = response.get('code')
    if response_code is None:
        response_code = 200
    return response, response_code


@bp.route('get-scraping-start', methods=['POST'])
def get_scraping_start():
    try:
        req = GetScrapingStartRequest(**request.get_json())
    except ValidationError as e:
        response = {
            'code': 400,
            'message': 'Validation error',
            'detail': e.errors()
        }
        app.logger.debug(response)
        return make_response(jsonify(response), 400)

    response = scraper_service.get_scraping_start(req)
    response_code = response.get('code')
    if response_code is None:
        response_code = 200
    return response, response_code


@bp.route('get-websites', methods=['GET'])
def get_websites():
    response = scraper_service.get_websites()
    response_code = response.get('code')
    if response_code is None:
        response_code = 200
    return response, response_code


@bp.route('set-delay', methods=['POST'])
def set_delay():
    try:
        req = SetDelayRequest(**request.get_json())
    except ValidationError as e:
        response = {
            'code': 400,
            'message': 'Validation error',
            'detail': e.errors()
        }
        app.logger.debug(response)
        return make_response(jsonify(response), 400)

    response = scraper_service.set_delay(req)

    response_code = response.get('code')
    if response_code is None:
        response_code = 200
    return response, response_code


@bp.route('set-scraping-start', methods=['POST'])
def set_scraping_start():
    try:
        req = SetScrapingStartRequest(**request.get_json())
    except ValidationError as e:
        response = {
            'code': 400,
            'message': 'Validation error',
            'detail': e.errors()
        }
        app.logger.debug(response)
        return make_response(jsonify(response), 400)

    response = scraper_service.set_scraping_start(req)

    response_code = response.get('code')
    if response_code is None:
        response_code = 200
    return response, response_code


app.register_blueprint(bp)


def create_app():
    return app
