from flask import Flask, request, make_response, jsonify, Blueprint
from pydantic import ValidationError
from flask_server.scraper_service import *


bp = Blueprint('route_prefix', __name__, template_folder='templates', url_prefix='/api/scraper')

app = Flask(__name__)

# logger = app.logger

logger = logging.getLogger('gunicorn.error')
app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

service = ScraperService(logger)


# Routes without prefix

@bp.route('/')
def hello():
    return 'Scraper service'


# Routes with prefix /api/scraper

@bp.route('/crawl', methods=['POST'])
def crawl():
    try:
        req = request.get_json()
        request_dto = CrawlRequest(**req)
    except ValidationError as e:
        response = {
            'code': 400,
            'message': 'Validation error',
            'detail': e.errors()
        }
        app.logger.debug(response)
        return make_response(jsonify(response), 400)

    service.crawl(request_dto)

    response = {'message': 'Crawl started', 'code': 200}
    return make_response(jsonify(response), 200)


@bp.route('/get-delay', methods=['POST'])
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

    result = service.get_delay(req)
    return result


@bp.route('/get-scraping-start', methods=['POST'])
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

    result = service.get_scraping_start(req)
    return result


@bp.route('/get-websites', methods=['GET'])
def get_websites():
    response = {
        "websites": service.get_websites()
    }
    return make_response(jsonify(response), 200)


@bp.route('/set-delay', methods=['POST'])
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

    service.set_delay(req)

    response = {'message': 'Done', 'code': 200}
    return make_response(jsonify(response), 200)


@bp.route('/set-scraping-start', methods=['POST'])
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

    service.set_scraping_start(req)

    response = {'message': 'Done', 'code': 200}
    return make_response(jsonify(response), 200)


app.register_blueprint(bp)


def create_app():
    return app
