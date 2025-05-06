import uuid
from django.db import models

# Create your models here.
class Conversation(models.Model):
    class Roles(models.TextChoices):
        OPEN = 'open', 'Open'
        CLOSED = 'closed', 'Closed'

    id = models.UUIDField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=6, choices=Roles.choices, default=Roles.OPEN)

class Message(models.Model):
    class Type(models.TextChoices):
        SENT = 'sent', 'Sent'
        RECEIVED = 'received', 'Received'

    id = models.UUIDField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    type = models.CharField(max_length=8, choices=Type.choices)