import logging
from time import sleep
from typing import Dict
from models.constants import Statuses, status_to_description
from flask import Flask, request, make_response, jsonify, Blueprint, redirect, url_for
from celery_app import func1, update_sentiments_task
from pydantic import ValidationError

from services.models import AnalyseRequest, UpdateSentimentRequest, TestRequest
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

running_update_sentiments_tasks: Dict[str, str] = {}
SERVER_SLEEP = 1


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


# @bp.route('update-sentiment', methods=['POST'])
# def update_sentiment():
#     try:
#         req = UpdateSentimentRequest(**request.get_json())
#     except ValidationError as e:
#         response = {
#             'code': 400,
#             'message': 'Validation error',
#             'detail': e.errors()
#         }
#         app.logger.debug(response)
#         return make_response(jsonify(response), 400)
#
#     sentiment_service.update(req)
#
#     response = {'message': 'Done', 'code': 200}
#     return make_response(jsonify(response), 200)


@bp.route('test', methods=['POST'])
def test():
    # req = request.get_json()
    # word = req['word']

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


# @bp.route('start-task', methods=['POST'])
# def start_task():
#     task = func1.delay()
#     return redirect(url_for('route_prefix.task_status', task_id=task.id))
#
#
# @bp.route('/status/<task_id>')
# def task_status(task_id):
#     task = func1.AsyncResult(task_id)
#     if task.state == 'PENDING':
#         sleep(SERVER_SLEEP)
#         response = {
#             'queue_state': task.state,
#             'status': 'Process is ongoing...',
#             'status_update': url_for('route_prefix.task_status', task_id=task.id)
#         }
#     else:
#         response = {
#             'queue_state': task.state,
#             'result': task.wait()
#         }
#     return jsonify(response)

@bp.route('/start-task', methods=['POST'])
def start_task():
    try:
        req = TestRequest(**request.get_json())
    except ValidationError as e:
        response = {
            'code': 400,
            'message': 'Validation error',
            'detail': e.errors()
        }
        app.logger.debug(response)
        return make_response(jsonify(response), 400)

    name = req.name
    task_id = running_update_sentiments_tasks.get(name, None)
    if task_id is None:
        # run new task
        task = func1.delay(name)
        running_update_sentiments_tasks[name] = task.id
        response = {
            'task_state': task.state,
            'task_status': 'Task created',
            'task_id': task.id
        }
        return response
    else:
        task = func1.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'task_state': task.state,
                'task_status': 'Task pending',
                'task_id': task.id
            }
            return response
        else:
            # forget old task
            task.forget()
            # run new task
            task = func1.delay(name)
            running_update_sentiments_tasks[name] = task.id
            response = {
                'task_state': task.state,
                'task_status': 'Task created',
                'task_id': task.id
            }
            return response


@bp.route('/status/<name>')
def task_status(name):
    task_id = running_update_sentiments_tasks.get(name, None)
    if task_id is None:
        # return empty task response
        response = {
            'task_state': 'EMPTY',
            'task_status': 'Task does not exist',
            'task_id': 0
        }
        return response
    else:
        task = func1.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'task_state': task.state,
                'task_status': 'Task pending',
                'task_id': task.id
            }
            return response
        else:
            # return task ended response
            response = {
                'task_state': task.state,
                'task_status': 'Task ended',
                'task_id': task.id
            }
            return response
    # task = func1.AsyncResult(task_id)
    # if task.state == 'PENDING':
    #     sleep(SERVER_SLEEP)
    #     response = {
    #         'queue_state': task.state,
    #         'status': 'Process is ongoing...',
    #         'status_update': url_for('route_prefix.task_status', task_id=task.id)
    #     }
    # else:
    #     response = {
    #         'queue_state': task.state,
    #         'result': task.wait()
    #     }
    # return jsonify(response)

@bp.route('/update-sentiments', methods=['POST'])
def update_sentiments():
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

    name = req.search_term
    task_id = running_update_sentiments_tasks.get(name, None)
    if task_id is None:
        # run new task
        task = update_sentiments_task.delay(name)
        running_update_sentiments_tasks[name] = task.id
        response = {
            'task_state': task.state,
            'task_status': status_to_description[Statuses.STARTED],
            'task_status_id': Statuses.STARTED.value,
            'task_id': task.id
        }
        return response
    else:
        task = update_sentiments_task.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'task_state': task.state,
                'task_status': status_to_description[Statuses.PENDING],
                'task_status_id': Statuses.PENDING.value,
                'task_id': task.id
            }
            return response
        else:
            # forget old task
            task.forget()
            # run new task
            task = update_sentiments_task.delay(name)
            running_update_sentiments_tasks[name] = task.id
            response = {
                'task_state': task.state,
                'task_status': status_to_description[Statuses.STARTED],
                'task_status_id': Statuses.STARTED.value,
                'task_id': task.id
            }
            return response


@bp.route('/update-sentiments/status/<search_term>')
def update_sentiments_status(search_term):
    task_id = running_update_sentiments_tasks.get(search_term, None)
    if task_id is None:
        # return empty task response
        response = {
            'task_state': 'EMPTY',
            'task_status': status_to_description[Statuses.NOT_CREATED],
            'task_status_id': Statuses.NOT_CREATED.value,
            'task_id': 0
        }
        return response
    else:
        task = update_sentiments_task.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'task_state': task.state,
                'task_status': status_to_description[Statuses.PENDING],
                'task_status_id': Statuses.PENDING.value,
                'task_id': task.id
            }
            return response
        else:
            # return task ended response
            response = {
                'task_state': task.state,
                'task_status': status_to_description[Statuses.ENDED],
                'task_status_id': Statuses.ENDED.value,
                'task_id': task.id
            }
            return response

@bp.route('/update-sentiments/get-all')
def update_sentiments_get_all():
    tasks = {}
    for key in running_update_sentiments_tasks.keys():
        task_id = running_update_sentiments_tasks.get(key)
        task = update_sentiments_task.AsyncResult(task_id)

        if task.state == 'PENDING':
            status = Statuses.PENDING
        else:
            status = Statuses.ENDED

        tasks[key] = {
            'task_state': task.state,
            'task_status': status_to_description[status],
            'task_status_id': status.value,
            'task_id': task.id
        }

    response = {
        "tasks": tasks
    }
    return response

# from celery_app import get_all_celery_tasks
#
# @bp.route('/get-all-tasks')
# def get_all_tasks():
#     get_all_celery_tasks()
#     return 'god'


app.register_blueprint(bp)


def create_app():
    return app
