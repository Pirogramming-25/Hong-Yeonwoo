import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .decorators import model_login_required
from .models import AIExecutionLog
from .services.combo import analyze_customer_feedback
from .services.moderator import analyze_toxicity
from .services.sentiment import analyze_sentiment
from .services.summarizer import summarize_text

logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def sentiment_page(request):
    histories = []

    if request.user.is_authenticated:
        histories = (
            AIExecutionLog.objects
            .filter(
                user=request.user,
                feature=AIExecutionLog.Feature.SENTIMENT,
            )[:5]
        )

    return render(request, "my_gpt/sentiment.html", {"histories": histories})


@ensure_csrf_cookie
@model_login_required
def summarize_page(request):
    histories = (
        AIExecutionLog.objects
        .filter(user=request.user, feature=AIExecutionLog.Feature.SUMMARIZE)[:5]
    )

    return render(request, "my_gpt/summarize.html", {"histories": histories})


@ensure_csrf_cookie
@model_login_required
def moderate_page(request):
    histories = (
        AIExecutionLog.objects
        .filter(user=request.user, feature=AIExecutionLog.Feature.MODERATE)[:5]
    )

    return render(request, "my_gpt/moderate.html", {"histories": histories})


@ensure_csrf_cookie
@model_login_required
def combo_page(request):
    histories = (
        AIExecutionLog.objects
        .filter(user=request.user, feature=AIExecutionLog.Feature.COMBO)[:5]
    )

    return render(request, "my_gpt/combo.html", {"histories": histories})


@require_POST
def sentiment_api(request):
    text = request.POST.get("text", "")

    try:
        result = analyze_sentiment(text)

        if request.user.is_authenticated:
            AIExecutionLog.objects.create(
                user=request.user,
                feature=AIExecutionLog.Feature.SENTIMENT,
                model_name=result["model_name"],
                input_text=text.strip(),
                output_text=result["label"],
                confidence=result["confidence"],
                raw_result=result["scores"],
            )

        return JsonResponse(
            {
                "ok": True,
                "label": result["label"],
                "confidence": round(result["confidence"] * 100, 2),
                "scores": [
                    {"label": item["label"], "score": round(item["score"] * 100, 2)}
                    for item in result["scores"]
                ],
                "saved": request.user.is_authenticated,
            }
        )

    except ValueError as error:
        return JsonResponse({"ok": False, "error": str(error)}, status=400)

    except Exception:
        logger.exception("Sentiment analysis failed")
        return JsonResponse(
            {
                "ok": False,
                "error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.",
            },
            status=500,
        )


@require_POST
@model_login_required
def summarize_api(request):
    text = request.POST.get("text", "")

    try:
        result = summarize_text(text)

        AIExecutionLog.objects.create(
            user=request.user,
            feature=AIExecutionLog.Feature.SUMMARIZE,
            model_name=result["model_name"],
            input_text=text.strip(),
            output_text=result["summary"],
            raw_result={
                "summary": result["summary"],
                "original_length": result["original_length"],
                "summary_length": result["summary_length"],
                "summary_ratio": result["summary_ratio"],
            },
        )

        return JsonResponse(
            {
                "ok": True,
                "summary": result["summary"],
                "original_length": result["original_length"],
                "summary_length": result["summary_length"],
                "summary_ratio": round(result["summary_ratio"], 2),
                "saved": True,
            }
        )

    except ValueError as error:
        return JsonResponse({"ok": False, "error": str(error)}, status=400)

    except Exception:
        logger.exception("Summarization failed")
        return JsonResponse(
            {
                "ok": False,
                "error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.",
            },
            status=500,
        )


@require_POST
@model_login_required
def moderate_api(request):
    text = request.POST.get("text", "")

    try:
        result = analyze_toxicity(text)

        AIExecutionLog.objects.create(
            user=request.user,
            feature=AIExecutionLog.Feature.MODERATE,
            model_name=result["model_name"],
            input_text=text.strip(),
            output_text=result["label"],
            confidence=result["score"],
            raw_result=result["scores"],
        )

        return JsonResponse(
            {
                "ok": True,
                "label": result["label"],
                "score": round(result["score"] * 100, 2),
                "scores": [
                    {"label": item["label"], "score": round(item["score"] * 100, 2)}
                    for item in result["scores"]
                ],
                "saved": True,
            }
        )

    except ValueError as error:
        return JsonResponse({"ok": False, "error": str(error)}, status=400)

    except Exception:
        logger.exception("Moderation failed")
        return JsonResponse(
            {
                "ok": False,
                "error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.",
            },
            status=500,
        )


@require_POST
@model_login_required
def combo_api(request):
    text = request.POST.get("text", "")

    try:
        result = analyze_customer_feedback(text)
        sentiment = result["sentiment"]
        toxicity = result["toxicity"]
        summary = result["summary"]

        AIExecutionLog.objects.create(
            user=request.user,
            feature=AIExecutionLog.Feature.COMBO,
            model_name=result["model_name"],
            input_text=text.strip(),
            output_text=result["judgement"],
            raw_result={
                "summary": summary,
                "sentiment": sentiment,
                "toxicity": toxicity,
                "judgement": result["judgement"],
            },
        )

        return JsonResponse(
            {
                "ok": True,
                "input_text": result["input_text"],
                "summary": summary["summary"],
                "sentiment": {
                    "label": sentiment["label"],
                    "confidence": round(sentiment["confidence"] * 100, 2),
                },
                "toxicity": {
                    "label": toxicity["label"],
                    "score": round(toxicity["score"] * 100, 2),
                    "scores": [
                        {
                            "label": item["label"],
                            "score": round(item["score"] * 100, 2),
                        }
                        for item in toxicity["scores"]
                    ],
                },
                "judgement": result["judgement"],
                "saved": True,
            }
        )

    except ValueError as error:
        return JsonResponse({"ok": False, "error": str(error)}, status=400)

    except Exception:
        logger.exception("Combo analysis failed")
        return JsonResponse(
            {
                "ok": False,
                "error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.",
            },
            status=500,
        )
