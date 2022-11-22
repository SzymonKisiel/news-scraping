import json
from threading import Thread

from flask import Flask, request, make_response, jsonify
from pydantic import ValidationError

from modules import crawl as crawl_module
from flask_server.scraper_service import CrawlRequest, SetScrapingStartRequest, ScraperService, SetDelayRequest, GetDelayRequest, GetScrapingStartRequest

app = Flask(__name__)
service = ScraperService(app.logger)


@app.route('/')
def hello():
    return 'Scraper service'


@app.route('/test1')
def test_start():
    websites = ['fakt']

    p = crawl_module.crawl_websites(websites, crawls_amount=1)
    p.join()

    return 'started'


@app.route('/test2')
def test_start2():
    def do_work(value):
        # do something that takes a long time
        import time
        print('started work')
        time.sleep(value)
        print('done work')

    thread = Thread(target=do_work, kwargs={'value': request.args.get('value', 20)})
    thread.start()
    return 'started'


@app.route('/test3')
def test_start3():
    def do_work(value):
        print('started work')

        websites = ['fakt']

        p = crawl_module.crawl_websites(websites, crawls_amount=1)
        p.join()

        print('done work')

    thread = Thread(target=do_work, kwargs={'value': request.args.get('value', 20)})
    thread.start()
    return 'started'


@app.route('/test4')
def test4():
    websites = ['fakt']

    crawl_module.async_crawl_websites(websites, crawls_amount=1)

    return 'started'


@app.route('/api/scraper/crawl', methods=['POST'])
def crawl():
    try:
        req = request.get_json()
        request_dto = CrawlRequest(**req)
    except ValidationError as e:
        print(e.json())
        return make_response("Validation error", 400)

    service.crawl(request_dto)

    response = {'message': 'Crawl started', 'code': 'SUCCESS'}
    return make_response(jsonify(response), 200)


@app.route('/api/scraper/get-delay', methods=['POST'])
def get_delay():
    try:
        req = GetDelayRequest(**request.get_json())
    except ValidationError as e:
        print(e.json())
        return make_response("Validation error", 400)

    result = service.get_delay(req)
    return result


@app.route('/api/scraper/get-scraping-start', methods=['POST'])
def get_scraping_start():
    try:
        req = GetScrapingStartRequest(**request.get_json())
    except ValidationError as e:
        print(e.json())
        return make_response("Validation error", 400)

    result = service.get_scraping_start(req)
    return result


@app.route('/api/scraper/get-websites', methods=['GET'])
def get_websites():
    return service.get_websites()


@app.route('/api/scraper/set-delay', methods=['POST'])
def set_delay():
    try:
        req = SetDelayRequest(**request.get_json())
    except ValidationError as e:
        print(e.json())
        return make_response("Validation error", 400)

    service.set_delay(req)

    response = {'message': 'Done', 'code': 'SUCCESS'}
    return make_response(jsonify(response), 200)


@app.route('/api/scraper/set-scraping-start', methods=['POST'])
def set_scraping_start():
    try:
        req = SetScrapingStartRequest(**request.get_json())
    except ValidationError as e:
        print(e.json())
        return make_response("Validation error", 400)

    service.set_scraping_start(req)

    response = {'message': 'Done', 'code': 'SUCCESS'}
    return make_response(jsonify(response), 200)
