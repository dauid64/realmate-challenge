from django.urls import path
from rest_framework import routers

from conversation.views import WeebhookView

app_name = 'conversation'

urlpatterns = [
    path('webhook/', WeebhookView.as_view(), name='webhook'),
]
