import os
from functools import lru_cache

from dotenv import load_dotenv
from transformers import pipeline

from .common import get_pipeline_device

load_dotenv()

SUMMARIZER_MODEL_ID = os.getenv(
    "HF_SUMMARIZER_MODEL_ID",
    "sshleifer/distilbart-cnn-6-6",
)

HF_TOKEN = os.getenv("HF_TOKEN")


@lru_cache(maxsize=1)
def get_summarizer_pipeline():
    kwargs = {
        "task": "summarization",
        "model": SUMMARIZER_MODEL_ID,
        "device": get_pipeline_device(),
    }

    if HF_TOKEN:
        kwargs["token"] = HF_TOKEN

    return pipeline(**kwargs)


def summarize_text(text):
    text = text.strip()

    if len(text) < 100:
        raise ValueError("요약할 문서는 100자 이상 입력해주세요.")

    if len(text) > 5000:
        raise ValueError("문서는 5,000자 이하로 입력해주세요.")

    summarizer = get_summarizer_pipeline()
    result = summarizer(
        text,
        max_length=160,
        min_length=30,
        do_sample=False,
    )

    summary = result[0]["summary_text"].strip()
    original_length = len(text)
    summary_length = len(summary)
    summary_ratio = (summary_length / original_length) * 100

    return {
        "summary": summary,
        "original_length": original_length,
        "summary_length": summary_length,
        "summary_ratio": summary_ratio,
        "model_name": SUMMARIZER_MODEL_ID,
        "raw_result": result,
    }
