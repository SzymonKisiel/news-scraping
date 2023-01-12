from pydantic import BaseModel


class AnalyseRequest(BaseModel):
    text: str


class UpdateSentimentRequest(BaseModel):
    search_term: str


class TestRequest(BaseModel):
    name: str
