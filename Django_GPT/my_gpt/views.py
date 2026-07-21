import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .decorators import model_login_required
from .models import AIExecutionLog
from .services.sentiment import analyze_sentiment

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

    return render(
        request,
        "my_gpt/sentiment.html",
        {
            "histories": histories,
        },
    )


@model_login_required
def summarize_page(request):
    return render(request, "my_gpt/summarize.html")


@model_login_required
def moderate_page(request):
    return render(request, "my_gpt/moderate.html")


@model_login_required
def combo_page(request):
    return render(request, "my_gpt/combo.html")


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
                    {
                        "label": item["label"],
                        "score": round(item["score"] * 100, 2),
                    }
                    for item in result["scores"]
                ],
                "saved": request.user.is_authenticated,
            }
        )

    except ValueError as error:
        return JsonResponse(
            {
                "ok": False,
                "error": str(error),
            },
            status=400,
        )

    except Exception:
        logger.exception("Sentiment analysis failed")
        return JsonResponse(
            {
                "ok": False,
                "error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.",
            },
            status=500,
        )
