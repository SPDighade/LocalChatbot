# chatbot_project/chatbot_app/urls.py
from django.urls import path
from .views import home, chat

urlpatterns = [
    path('home/', home, name='home'),
    path('', chat, name='chat'),
]
