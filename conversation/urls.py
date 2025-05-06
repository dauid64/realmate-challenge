from django.urls import path

from conversation.views import ConversationDetailView, WeebhookView, ConversationDetailHTMLView

app_name = 'conversation'

urlpatterns = [
    path('webhook/', WeebhookView.as_view(), name='webhook'),
    path("conversations/<uuid:id>/", ConversationDetailView.as_view(), name="detail"),
    path("conversations/<uuid:id>/html/", ConversationDetailHTMLView.as_view(), name="detail-html"),
]
