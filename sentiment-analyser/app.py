import logging
from flask import Flask, request, make_response, jsonify, Blueprint
from pydantic import ValidationError

from services.models import AnalyseRequest
from services.sentiment_analyse_service import SentimentAnalyseService

bp = Blueprint('route_prefix', __name__, template_folder='templates', url_prefix='/api/sentiment-analyser')

app = Flask(__name__)

# local development logger
# logger = app.logger

# production logger
# logger = logging.getLogger('gunicorn.error')
# app.logger.handlers = logger.handlers
# app.logger.setLevel(logger.level)

app.logger.setLevel('DEBUG')

sentiment_analyse_service = SentimentAnalyseService(app.logger)


@bp.route('/')
def hello():
    return 'Command handler service'


# @bp.route('crawl', methods=['POST'])
# def crawl():
#     try:
#         req = request.get_json()
#         request_dto = CrawlRequest(**req)
#     except ValidationError as e:
#         print(e.json())
#         return make_response("Validation error", 400)
#
#     scraper_service.crawl(request_dto)
#
#     ok_response = {'message': 'Crawl started', 'code': 200}
#     return jsonify(ok_response), 200

@bp.route('analyse', methods=['POST'])
def analyse():
    try:
        req = request.get_json()
        request_dto = AnalyseRequest(**req)
    except ValidationError as e:
        print(e.json())
        return make_response("Validation error", 400)

    sentiment = sentiment_analyse_service.analyse(request_dto)

    # ok_response = {'message': 'Crawl started', 'code': 200}
    return sentiment.to_dictionary()


@bp.route('test', methods=['POST'])
def test():
    req = request.get_json()
    word = req['word']
    # search_service.search(word)

    # s_repo = SentimentService(app.logger)
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

    # sent_service = SentimentService(app.logger)
    # sent_service.test()

    return 'good'


app.register_blueprint(bp)


def create_app():
    return app
