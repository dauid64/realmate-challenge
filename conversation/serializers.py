from rest_framework import serializers
from conversation.models import Conversation, Message

class WebHookSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["NEW_CONVERSATION", "NEW_MESSAGE", "CLOSE_CONVERSATION"])
    timestamp = serializers.DateTimeField()
    data = serializers.DictField()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'type', 'created_at', 'started_at']
        ordering = ['started_at']
    

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['state', 'messages']
