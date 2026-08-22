from transformers import pipeline

from .schemas import (
    IntentResponse,
    IntentScore,
)


DEFAULT_INTENTS = [
    "产品咨询",
    "订单状态",
    "物流",
    "退货",
    "退款",
    "取消订单",
    "产品适配",
    "产品比较",
    "付款问题",
    "投诉",
    "其他",
]


class MultilingualIntentClassifier:
    MODEL_ID = (
        "joeddav/"
        "xlm-roberta-large-xnli"
    )

    MODEL_VERSION = (
        "UNPINNED_INITIAL"
    )

    def __init__(self):
        self.classifier = pipeline(
            "zero-shot-classification",
            model=self.MODEL_ID,
        )

    def classify(
        self,
        text: str,
        candidate_labels=None,
    ) -> IntentResponse:
        labels = (
            candidate_labels
            or DEFAULT_INTENTS
        )

        result = self.classifier(
            text,
            labels,
            multi_label=False,
        )

        predictions = [
            IntentScore(
                label=label,
                score=float(score),
            )
            for label, score
            in zip(
                result["labels"],
                result["scores"],
            )
        ]

        return IntentResponse(
            model_id=self.MODEL_ID,
            model_version=
                self.MODEL_VERSION,
            predictions=
                predictions,
        )