import os
from functools import lru_cache

from dotenv import load_dotenv
from transformers import pipeline

from .common import get_pipeline_device

load_dotenv()

MODERATOR_MODEL_ID = os.getenv(
    "HF_MODERATOR_MODEL_ID",
    "unitary/toxic-bert",
)

HF_TOKEN = os.getenv("HF_TOKEN")


@lru_cache(maxsize=1)
def get_moderator_pipeline():
    kwargs = {
        "task": "text-classification",
        "model": MODERATOR_MODEL_ID,
        "top_k": None,
        "device": get_pipeline_device(),
    }

    if HF_TOKEN:
        kwargs["token"] = HF_TOKEN

    return pipeline(**kwargs)


def analyze_toxicity(text):
    text = text.strip()

    if not text:
        raise ValueError("분석할 문장을 입력해주세요.")

    if len(text) > 1000:
        raise ValueError("문장은 1,000자 이하로 입력해주세요.")

    moderator = get_moderator_pipeline()
    result = moderator(text)

    scores = result[0] if result and isinstance(result[0], list) else result
    scores = sorted(scores, key=lambda item: item["score"], reverse=True)
    top = scores[0]

    return {
        "label": top["label"].lower(),
        "score": top["score"],
        "scores": [
            {
                "label": item["label"].lower(),
                "score": item["score"],
            }
            for item in scores
        ],
        "model_name": MODERATOR_MODEL_ID,
    }
