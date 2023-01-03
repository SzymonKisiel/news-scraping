import json
import logging
from flask import Flask, request, make_response, jsonify, Blueprint
from flask_cors import CORS
from mysql.connector import IntegrityError, DatabaseError
from pydantic import ValidationError

from database.repositories.client_repository import ClientRepository
from database.repositories.search_term_repository import SearchTermRepository
from database.repositories.sentiment_repository import SentimentRepository
from models.sentiment import Sentiment
from services.client_service import ClientService
from services.search_service import SearchService
from services.scraper_service import ScraperService
from services.models import *


# def setup_logging(level=logging.INFO):
#     app.logger.setLevel(level)
#
#     # Here we define our formatter
#     FORMAT = "%(relativeCreated)6d %(threadName)15s %(filename)25s:%(lineno)4s - %(name)30s:%(funcName)20s() %(levelname)-5.5s : %(message)s"
#     formatter = logging.Formatter(FORMAT)
#
#     consoleHandler = logging.StreamHandler(stream=sys.stdout)
#     consoleHandler.setFormatter(formatter)
#     consoleHandler.setLevel(level)
#
#     app.logger.addHandler(consoleHandler)
from services.search_term_service import SearchTermService
from services.sentiment_service import SentimentService

bp = Blueprint('route_prefix', __name__, template_folder='templates', url_prefix='/api/command-handler')

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# local development logger
# logger = app.logger

# production logger
# logger = logging.getLogger('gunicorn.error')
# app.logger.handlers = logger.handlers
# app.logger.setLevel(logger.level)

app.logger.setLevel('DEBUG')

scraper_service = ScraperService(app.logger)
search_service = SearchService(app.logger)
client_service = ClientService(app.logger)
sentiment_service = SentimentService(app.logger)
search_term_service = SearchTermService(app.logger)


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


# @bp.route('search-test', methods=['POST'])
# def search():
#     req = request.get_json()
#     word = req['word']
#     search_service.search(word)
#
#     return 'good'


@bp.route('test', methods=['POST'])
def test():
    req = request.get_json()
    word = req['word']
    # search_service.search(word)

    # c_repo = ClientRepository(app.logger)
    # c_repo.get_all_clients()
    # c_repo.add_client('ClientTest')
    # c_repo.get_all_clients()

    # st_repo = SearchTermRepository(app.logger)
    # st_repo.get_all_by_client_id(1)
    # st_repo.get_all_by_client_name('Client1')
    # try:
    #     st_repo.add_search_term_to_client('ClientTest', 'Test')
    # except DatabaseError as e:
    #     print("Error: {}".format(e))
    #     return {"message": e.msg}

    # s_repo = SentimentRepository(app.logger)
    # s_repo.get_all_by_client_id(1)
    # s_repo.get_all_by_client_name('Client1')
    # s_repo.get_all_by_search_term_id(1)
    # s_repo.get_all_by_search_term_name('McDonald')
    # new_sentiment = Sentiment(
    #     article_id=1257,
    #     search_term_id=1,
    #     sentence='Testowa ocena',
    #     positive_score=0.25,
    #     neutral_score=0.5,
    #     negative_score=0.25,
    #     overall_sentiment=1
    # )
    # s_repo.count__sentiments(1257, 1)
    # s_repo.insert_sentiment(new_sentiment)

    sent_service = SentimentService(app.logger)
    sent_service.test()

    return 'good'


@bp.route('update-sentiment', methods=['POST'])
def update_sentiment():
    try:
        req = UpdateSentimentRequest(**request.get_json())
    except ValidationError as e:
        response = {
            'code': 400,
            'message': 'Validation error',
            'detail': e.errors()
        }
        app.logger.debug(response)
        return make_response(jsonify(response), 400)

    sentiment_service.update(req)

    response = {'message': 'Done', 'code': 200}
    return make_response(jsonify(response), 200)


@bp.route('add-client', methods=['POST'])
def add_client():
    try:
        req = AddClientRequest(**request.get_json())
    except ValidationError as e:
        response = {
            'code': 400,
            'message': 'Validation error',
            'detail': e.errors()
        }
        app.logger.debug(response)
        return make_response(jsonify(response), 400)

    try:
        client_service.add_client(req)
    except DatabaseError as e:
        print("Error: {}".format(e))
        return {"message": e.msg}

    response = {'message': 'Done', 'code': 200}
    return make_response(jsonify(response), 200)


@bp.route('add-search-term', methods=['POST'])
def add_search_term():
    try:
        req = AddSearchTermRequest(**request.get_json())
    except ValidationError as e:
        response = {
            'code': 400,
            'message': 'Validation error',
            'detail': e.errors()
        }
        app.logger.debug(response)
        return make_response(jsonify(response), 400)

    try:
        client_service.add_search_term(req)
    except DatabaseError as e:
        print("Error: {}".format(e))
        return {"message": e.msg}

    response = {'message': 'Done', 'code': 200}
    return make_response(jsonify(response), 200)


@bp.route('get-all-sentiments', methods=['GET'])
def get_all_sentiments():
    search_term = request.args.get('term')
    if search_term is None:
        response = {
            'code': 400,
            'message': 'Invalid parameters',
            'detail': '"term" parameter is required'
        }
        app.logger.debug(response)
        return make_response(jsonify(response), 400)

    sentiments = sentiment_service.get_all_by_search_term(search_term)
    sentiments_result = []
    for sentiment in sentiments:
        sentiments_result.append(sentiment.to_dict())

    response = {
        "sentiments": sentiments_result
    }
    return make_response(jsonify(response), 200)


@bp.route('get-all-search-terms', methods=['GET'])
def get_all_search_terms():
    client_name = request.args.get('client_name')
    if client_name is None:
        response = {
            'code': 400,
            'message': 'Invalid parameters',
            'detail': '"client_name" parameter is required'
        }
        app.logger.debug(response)
        return make_response(jsonify(response), 400)

    search_terms = search_term_service.get_all_by_client_name(client_name)
    search_term_names = [term.search_term for term in search_terms]

    response = {
        "search_terms": search_term_names
    }
    return make_response(jsonify(response), 200)


@bp.route('get-all-clients', methods=['GET'])
def get_all_clients():
    clients = client_service.get_all()
    clients_json = [client.to_dict() for client in clients]

    response = {
        "clients": clients_json
    }
    return make_response(jsonify(response), 200)


app.register_blueprint(bp)


def create_app():
    return app
