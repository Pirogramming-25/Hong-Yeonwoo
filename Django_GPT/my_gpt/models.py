from django.conf import settings
from django.db import models


class AIExecutionLog(models.Model):
    class Feature(models.TextChoices):
        SENTIMENT = "sentiment", "Sentiment"
        SUMMARIZE = "summarize", "Summarize"
        MODERATE = "moderate", "Moderate"
        COMBO = "combo", "Combo"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_execution_logs",
        null=True,
        blank=True,
    )
    feature = models.CharField(
        max_length=20,
        choices=Feature.choices,
    )
    model_name = models.CharField(max_length=200)
    input_text = models.TextField()
    output_text = models.TextField()
    confidence = models.FloatField(null=True, blank=True)
    raw_result = models.JSONField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["feature", "-created_at"]),
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.feature} - {self.model_name} - {self.created_at:%Y-%m-%d %H:%M}"
