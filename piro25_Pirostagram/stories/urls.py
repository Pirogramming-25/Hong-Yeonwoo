from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('create/', views.create_story, name='create_story'),
    path('delete/<int:story_id>/', views.delete_story, name='delete_story'),
]