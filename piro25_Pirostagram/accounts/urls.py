from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/<str:username>/', views.profile, name='profile'),
    path('search/', views.user_search, name='user_search'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
]