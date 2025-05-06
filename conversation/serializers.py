from rest_framework import serializers

class WebHookSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["NEW_CONVERSATION", "NEW_MESSAGE", "CLOSE_CONVERSATION"])
    timestamp = serializers.DateTimeField()
    data = serializers.DictField()
