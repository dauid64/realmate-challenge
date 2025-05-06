from uuid import uuid4
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from conversation.models import Conversation, Message

class TestConversationDetail(TestCase):
    def setUp(self):
        conv = Conversation.objects.create(id=uuid4(), started_at=timezone.now())
        initial_messages = [
            {
                "id": uuid4(),
                "started_at": timezone.now(),
                "content": "Primeira mensagem",
                "type": "received"
            },
            {
                "id": uuid4(),
                "started_at": timezone.now(),
                "content": "Resposta",
                "type": "sent"
            }
        ]
        for message in initial_messages:
            Message.objects.create(
                id=message["id"],
                conversation=conv,
                started_at=message["started_at"],
                content=message["content"],
                type=message["type"]
            )
        self.conv = conv
        self.msgs = initial_messages
        
    def test_conversation_detail_html_view_template_used(self):
        url = reverse("conversation:detail-html", kwargs={"id": str(self.conv.id)})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation/pages/detail.html')
    
    def test_conversation_detail_html_view_not_found(self):
        fake_id = uuid4()
        url = reverse("conversation:detail-html", kwargs={"id": str(fake_id)})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
    
    def test_conversation_detail_html_view_context(self):
        url = reverse("conversation:detail-html", kwargs={"id": str(self.conv.id)})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['conversation'], self.conv)
        self.assertEqual(len(response.context['messages']), 2)
        self.assertEqual(response.context['messages'][0].id, self.msgs[0]["id"])
        self.assertEqual(response.context['messages'][1].id, self.msgs[1]["id"])

    def test_conversation_detail_html_view_no_messages(self):
        # Create a conversation without messages
        conv = Conversation.objects.create(id=uuid4(), started_at=timezone.now())
        url = reverse("conversation:detail-html", kwargs={"id": str(conv.id)})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['conversation'], conv)
        self.assertEqual(len(response.context['messages']), 0)
        self.assertContains(response, "Nenhuma mensagem nesta conversa")
        