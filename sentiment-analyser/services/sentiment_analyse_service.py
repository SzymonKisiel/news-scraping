import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel
from scipy.special import softmax

from models.sentiment_score import SentimentScore
from models.constants import id2label, label2id
from services.models import AnalyseRequest


class SentimentAnalyseService:
    logger: logging.Logger

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.tokenizer = AutoTokenizer.from_pretrained("Voicelab/herbert-base-cased-sentiment")
        self.model = AutoModelForSequenceClassification.from_pretrained("Voicelab/herbert-base-cased-sentiment")

    def analyse(self, analyse_request: AnalyseRequest) -> SentimentScore:
        text_input = analyse_request.text
        encoding = self.tokenizer(
            text_input,
            add_special_tokens=True,
            return_token_type_ids=True,
            truncation=True,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
        )

        output = self.model(**encoding)
        scores = output[0][0].detach().numpy()
        # print(scores)

        # prediction = self.id2label[np.argmax(scores)]
        # print(prediction)

        scores = softmax(scores)
        # print(scores)

        # prediction = self.id2label[np.argmax(scores)]
        # print(prediction)

        negative_score = scores[label2id['negative']]
        neutral_score = scores[label2id['neutral']]
        positive_score = scores[label2id['positive']]

        sentiment = SentimentScore(
            negative_score=negative_score,
            neutral_score=neutral_score,
            positive_score=positive_score
        )
        # print(f"negative: {negative_score}")
        # print(f"neutral: {neutral_score}")
        # print(f"positive: {positive_score}")

        # return output
        # return prediction
        return sentiment
