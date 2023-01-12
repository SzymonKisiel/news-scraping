import spacy
from typing import List


class Sentencizer:
    def __init__(self):
        self.nlp = spacy.load('pl_core_news_md')
        self.nlp.add_pipe('sentencizer')

    def sentecize(self, text: str) -> List[str]:
        doc = self.nlp(text)
        sentences = [sentence.text.strip() for sentence in doc.sents]
        return sentences
