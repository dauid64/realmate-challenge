import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from conversation.models import Conversation, Message
from uuid import UUID
from django.utils import timezone
from rest_framework.test import APITestCase

class TestWebhook(APITestCase):
    def test_create_new_conversation(self):
        data = {
            "type": "NEW_CONVERSATION",
            "timestamp": "2025-02-21T10:20:41.349308",
            "data": {
                "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
            }
        }
        response = self.client.post("/webhook/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Conversation.objects.filter(id=data["data"]["id"]).exists())

    def test_prevent_duplicate_conversation(self):
        conv_id = UUID("6a41b347-8d80-4ce9-84ba-7af66f369f6a")
        Conversation.objects.create(id=conv_id, started_at=timezone.now())
        data = {
            "type": "NEW_CONVERSATION",
            "timestamp": "2025-02-21T10:20:41.349308",
            "data": {"id": str(conv_id)}
        }
        response = self.client.post("/webhook/", data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Conversation already exists")

    def test_receive_new_message(self):
        conv_id = UUID("6a41b347-8d80-4ce9-84ba-7af66f369f6a")
        Conversation.objects.create(id=conv_id, started_at=timezone.now())
        data = {
            "type": "NEW_MESSAGE",
            "timestamp": "2025-02-21T10:20:42.349308",
            "data": {
                "id": "49108c71-4dca-4af3-9f32-61bc745926e2",
                "direction": "RECEIVED",
                "content": "Olá, tudo bem?",
                "conversation_id": str(conv_id)
            }
        }
        response = self.client.post("/webhook/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Message.objects.filter(id=data["data"]["id"]).exists())

    def test_do_not_accept_messages_in_closed_conversation(self):
        conv_id = UUID("6a41b347-8d80-4ce9-84ba-7af66f369f6a")
        Conversation.objects.create(id=conv_id, started_at=timezone.now(), state="closed")
        data = {
            "type": "NEW_MESSAGE",
            "timestamp": "2025-02-21T10:20:44.349308",
            "data": {
                "id": "16b63b04-60de-4257-b1a1-20a5154abc6d",
                "direction": "SENT",
                "content": "Tudo ótimo e você?",
                "conversation_id": str(conv_id)
            }
        }
        response = self.client.post("/webhook/", data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Conversation is closed")


    def test_prevent_duplicate_messages(self):
        conv_id = UUID("6a41b347-8d80-4ce9-84ba-7af66f369f6a")
        msg_id = UUID("16b63b04-60de-4257-b1a1-20a5154abc6d")
        conv = Conversation.objects.create(id=conv_id, started_at=timezone.now())
        Message.objects.create(id=msg_id, conversation=conv, started_at=timezone.now(), content="Mensagem", type="sent")
        data = {
            "type": "NEW_MESSAGE",
            "timestamp": "2025-02-21T10:20:44.349308",
            "data": {
                "id": str(msg_id),
                "direction": "SENT",
                "content": "Tudo ótimo e você?",
                "conversation_id": str(conv_id)
            }
        }
        response = self.client.post("/webhook/", data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Message already exists")

    def test_close_conversation(self):
        conv_id = UUID("6a41b347-8d80-4ce9-84ba-7af66f369f6a")
        conv = Conversation.objects.create(id=conv_id, started_at=timezone.now())
        data = {
            "type": "CLOSE_CONVERSATION",
            "timestamp": "2025-02-21T10:20:45.349308",
            "data": {"id": str(conv_id)}
        }
        response = self.client.post("/webhook/", data, format="json")
        conv.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(conv.state, "closed")
        self.assertIsNotNone(conv.closed_at)

    def test_close_nonexistent_conversation(self):
        data = {
            "type": "CLOSE_CONVERSATION",
            "timestamp": "2025-02-21T10:20:45.349308",
            "data": {"id": "00000000-0000-0000-0000-000000000000"}
        }
        response = self.client.post("/webhook/", data, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "Conversation not found")
