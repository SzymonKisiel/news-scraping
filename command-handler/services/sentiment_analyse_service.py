import logging

import requests

from models.sentiment_score import SentimentScore
from services.models import AnalyseRequest, UpdateSentimentRequest
from utils.env_variables import get_sentiment_analyser_api


class SentimentAnalyseService:
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.api_url = get_sentiment_analyser_api()

    # def analyse(self, sentence: str) -> SentimentScore:
    #     self.logger.debug('analyse')
    #
    #     action = '/analyse'
    #     url = self.api_url + action
    #     request = AnalyseRequest(text=sentence)
    #     request_dict = request.dict()
    #
    #     response = requests.post(url, json=request_dict)
    #     score_json = response.json()
    #     score = SentimentScore(
    #         negative_score=score_json['negative_score'],
    #         neutral_score=score_json['neutral_score'],
    #         positive_score=score_json['positive_score']
    #     )
    #     return score

    def update_sentiments(self, request: UpdateSentimentRequest):
        self.logger.debug('update_sentiments')

        action = '/update-sentiments'
        url = self.api_url + action

        request_dict = request.dict()

        response = requests.post(url, json=request_dict)
        return response.json()

    def update_sentiments_status(self, search_term: str):
        self.logger.debug('update_sentiments_status')

        action = '/update-sentiments/status/' + search_term
        url = self.api_url + action

        response = requests.get(url)
        return response.json()

    def update_sentiments_get_all(self):
        self.logger.debug('update_sentiments_get_all')

        action = '/update-sentiments/get-all'
        url = self.api_url + action

        response = requests.get(url)
        return response.json()
