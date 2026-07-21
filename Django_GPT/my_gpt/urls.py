from django.urls import path

from .views import combo_page, moderate_page, sentiment_api, sentiment_page, summarize_page

app_name = "my_gpt"

urlpatterns = [
    path("", sentiment_page, name="main"),
    path("sentiment/", sentiment_page, name="sentiment"),
    path("summarize/", summarize_page, name="summarize"),
    path("moderate/", moderate_page, name="moderate"),
    path("combo/", combo_page, name="combo"),
    path("api/sentiment/", sentiment_api, name="sentiment_api"),
]
