from .moderator import analyze_toxicity
from .sentiment import analyze_sentiment
from .summarizer import SUMMARIZER_MODEL_ID, summarize_text


def build_overall_judgement(sentiment, toxicity):
    sentiment_label = sentiment["label"]
    toxicity_label = toxicity["label"]
    toxicity_score = toxicity["score"]

    if sentiment_label == "negative":
        sentiment_description = "부정적인 평가를 포함합니다."
    elif sentiment_label == "positive":
        sentiment_description = "긍정적인 평가를 포함합니다."
    else:
        sentiment_description = "중립적인 평가로 보입니다."

    if toxicity_score >= 0.5:
        toxicity_description = f"유해 표현 가능성이 높습니다. 가장 높은 위험 레이블은 {toxicity_label}입니다."
    elif toxicity_score >= 0.2:
        toxicity_description = f"일부 유해 표현 가능성이 있습니다. 가장 높은 위험 레이블은 {toxicity_label}입니다."
    else:
        toxicity_description = "심각한 유해 표현 가능성은 낮습니다."

    return f"{sentiment_description} {toxicity_description}"


def analyze_customer_feedback(text):
    text = text.strip()

    if len(text) < 200:
        raise ValueError("복합 분석할 문서는 200자 이상 입력해주세요.")

    if len(text) > 5000:
        raise ValueError("문서는 5,000자 이하로 입력해주세요.")

    summary = summarize_text(
        text,
        max_length=180,
        min_length=40,
        do_sample=True,
        top_p=0.9,
        temperature=0.8,
    )
    sentiment = analyze_sentiment(summary["summary"])
    toxicity = analyze_toxicity(summary["summary"])
    judgement = build_overall_judgement(sentiment, toxicity)

    return {
        "input_text": text,
        "summary": summary,
        "sentiment": sentiment,
        "toxicity": toxicity,
        "judgement": judgement,
        "model_name": (
            f"{SUMMARIZER_MODEL_ID} -> "
            f"{sentiment['model_name']} -> "
            f"{toxicity['model_name']}"
        ),
    }
