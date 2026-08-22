from typing import List, Optional
from pydantic import BaseModel, Field


class SentimentRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class SentimentResponse(BaseModel):
    model_id: str
    model_version: str
    label: str
    positive_probability: float
    negative_probability: float


class IntentRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    candidate_labels: Optional[List[str]] = None


class IntentScore(BaseModel):
    label: str
    score: float


class IntentResponse(BaseModel):
    model_id: str
    model_version: str
    predictions: List[IntentScore]


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    candidate_labels: Optional[List[str]] = None


class AnalyzeResponse(BaseModel):
    sentiment: SentimentResponse
    intent: IntentResponse