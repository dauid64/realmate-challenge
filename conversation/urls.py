from django.urls import path

from conversation.views import ConversationDetailView, WeebhookView

app_name = 'conversation'

urlpatterns = [
    path('webhook/', WeebhookView.as_view(), name='webhook'),
    path("conversations/<uuid:id>/", ConversationDetailView.as_view(), name="conversation-detail"),
]
