from django.urls import reverse
from conversation.models import Conversation, Message
from uuid import uuid4
from django.utils import timezone
from rest_framework.test import APITestCase

class TestConversationDetail(APITestCase):
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

    def test_retrieve_existing_conversation_with_messages(self):
        url = reverse("conversation:detail", kwargs={"id": str(self.conv.id)})
        response = self.client.get(url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["state"], "open")
        self.assertEqual(len(response.data["messages"]), 2)
        self.assertTrue(all("id" in msg and "content" in msg for msg in response.data["messages"]))
        self.assertEqual(response.data["messages"][0]["id"], str(self.msgs[0]["id"]))
        self.assertEqual(response.data["messages"][1]["id"], str(self.msgs[1]["id"]))

    def test_conversation_not_found(self):
        fake_id = uuid4()
        url = reverse("conversation:detail", kwargs={"id": str(fake_id)})
        response = self.client.get(url)

        assert response.status_code == 404
