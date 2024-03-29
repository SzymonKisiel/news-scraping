from typing import List, Optional
from pydantic import BaseModel


class CrawlRequest(BaseModel):
    websites: List[str] = []
    crawls_amount: Optional[int]
    due_time: Optional[str]
    run_time: Optional[int]


class GetDelayRequest(BaseModel):
    websites: List[str]


class GetScrapingStartRequest(BaseModel):
    websites: List[str]


class SetDelayRequest(BaseModel):
    websites: List[str]
    delay: int


class SetScrapingStartRequest(BaseModel):
    websites: List[str]
    date: str
