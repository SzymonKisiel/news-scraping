import numpy


class SentimentScore:
    negative_score: float
    neutral_score: float
    positive_score: float

    def __init__(self, negative_score: float, neutral_score: float, positive_score: float):
        self.negative_score = negative_score
        self.neutral_score = neutral_score
        self.positive_score = positive_score

    def to_overall_sentiment_id(self) -> int:
        scores = [self.negative_score, self.neutral_score, self.positive_score]
        overall_sentiment_id: int = int(numpy.argmax(scores))
        return overall_sentiment_id
