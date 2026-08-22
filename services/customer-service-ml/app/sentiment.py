import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

from .schemas import SentimentResponse


class ChineseSentimentAnalyzer:
    MODEL_ID = "uer/roberta-base-finetuned-jd-binary-chinese"
    MODEL_VERSION = "UNPINNED_INITIAL"

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.MODEL_ID
        )

        self.model = (
            AutoModelForSequenceClassification
            .from_pretrained(
                self.MODEL_ID
            )
        )

        self.model.eval()

    def analyze(
        self,
        text: str,
    ) -> SentimentResponse:
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=256,
        )

        with torch.no_grad():
            outputs = self.model(
                **inputs
            )

            probabilities = torch.softmax(
                outputs.logits,
                dim=-1,
            )[0]

        labels = (
            self.model.config.id2label
            or {}
        )

        scores = {
            labels.get(
                index,
                str(index),
            ): float(
                probability.item()
            )
            for index, probability
            in enumerate(
                probabilities
            )
        }

        normalized = {
            key.lower():
                value
            for key, value
            in scores.items()
        }

        positive = (
            normalized.get("positive")
            or normalized.get("pos")
        )

        negative = (
            normalized.get("negative")
            or normalized.get("neg")
        )

        # Do not silently assume class order if
        # model metadata is ambiguous.
        if (
            positive is None
            or negative is None
        ):
            if len(probabilities) != 2:
                raise RuntimeError(
                    "Sentiment model labels "
                    "could not be interpreted safely."
                )

            # Initial compatibility fallback.
            # This must be qualified against
            # model documentation/test fixtures.
            negative = float(
                probabilities[0].item()
            )

            positive = float(
                probabilities[1].item()
            )

        label = (
            "POSITIVE"
            if positive >= negative
            else "NEGATIVE"
        )

        return SentimentResponse(
            model_id=self.MODEL_ID,
            model_version=
                self.MODEL_VERSION,
            label=label,
            positive_probability=
                positive,
            negative_probability=
                negative,
        )