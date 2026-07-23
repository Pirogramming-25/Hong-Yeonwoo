import os
from functools import lru_cache

from dotenv import load_dotenv
from transformers import pipeline

from .common import get_pipeline_device

load_dotenv()

SENTIMENT_MODEL_ID = os.getenv(
    "HF_SENTIMENT_MODEL_ID",
    "cardiffnlp/twitter-roberta-base-sentiment-latest",
)

HF_TOKEN = os.getenv("HF_TOKEN")


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    kwargs = {
        "task": "text-classification",
        "model": SENTIMENT_MODEL_ID,
        "top_k": None,
        "device": get_pipeline_device(),
    }

    if HF_TOKEN:
        kwargs["token"] = HF_TOKEN

    return pipeline(**kwargs)


def analyze_sentiment(text):
    text = text.strip()

    if not text:
        raise ValueError("분석할 문장을 입력해주세요.")

    if len(text) > 1000:
        raise ValueError("입력 문장은 최대 1,000자까지 가능합니다.")

    classifier = get_sentiment_pipeline()
    result = classifier(text)

    scores = result[0] if result and isinstance(result[0], list) else result
    scores = sorted(scores, key=lambda item: item["score"], reverse=True)

    best = scores[0]

    return {
        "label": best["label"].lower(),
        "confidence": best["score"],
        "scores": [
            {
                "label": item["label"].lower(),
                "score": item["score"],
            }
            for item in scores
        ],
        "model_name": SENTIMENT_MODEL_ID,
    }
