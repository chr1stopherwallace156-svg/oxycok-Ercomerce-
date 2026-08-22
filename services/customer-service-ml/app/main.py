from fastapi import FastAPI

from .intent import (
    MultilingualIntentClassifier,
)

from .schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    IntentRequest,
    IntentResponse,
    SentimentRequest,
    SentimentResponse,
)

from .sentiment import (
    ChineseSentimentAnalyzer,
)


app = FastAPI(
    title=(
        "OXYCOK Customer "
        "Service ML"
    ),
    version="0.1.0",
)


sentiment_model = (
    ChineseSentimentAnalyzer()
)

intent_model = (
    MultilingualIntentClassifier()
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service":
            "customer-service-ml",
        "sentiment_model":
            sentiment_model.MODEL_ID,
        "intent_model":
            intent_model.MODEL_ID,
    }


@app.post(
    "/sentiment",
    response_model=
        SentimentResponse,
)
def sentiment(
    request:
        SentimentRequest,
):
    return sentiment_model.analyze(
        request.text
    )


@app.post(
    "/intent",
    response_model=
        IntentResponse,
)
def intent(
    request:
        IntentRequest,
):
    return intent_model.classify(
        request.text,
        request.candidate_labels,
    )


@app.post(
    "/analyze",
    response_model=
        AnalyzeResponse,
)
def analyze(
    request:
        AnalyzeRequest,
):
    sentiment_result = (
        sentiment_model.analyze(
            request.text
        )
    )

    intent_result = (
        intent_model.classify(
            request.text,
            request.candidate_labels,
        )
    )

    return AnalyzeResponse(
        sentiment=
            sentiment_result,
        intent=
            intent_result,
    )