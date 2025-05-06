from rest_framework.views import APIView
from rest_framework.response import Response

from conversation.models import Conversation, Message
from conversation.serializers import ConversationSerializer, WebHookSerializer
from rest_framework.generics import RetrieveAPIView

from rest_framework import status


class WeebhookView(APIView):
    def post(self, request):
        serializer = WebHookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        type_ = serializer.validated_data["type"]
        data = serializer.validated_data["data"]
        timestamp = serializer.validated_data["timestamp"]

        if type_ == "NEW_CONVERSATION":
            conv_id = data["id"]
            if Conversation.objects.filter(id=conv_id).exists():
                return Response({"error": "Conversation already exists"}, status=status.HTTP_400_BAD_REQUEST)
            Conversation.objects.create(id=conv_id, started_at=timestamp)
            return Response(status=status.HTTP_201_CREATED)
        
        if type_ == "NEW_MESSAGE":
            conv_id = data["conversation_id"]
            msg_id = data["id"]
            conversation = Conversation.objects.filter(id=conv_id).first()

            if not conversation:
                return Response({"error": "Conversation not found"}, status=404)
            if conversation.state == Conversation.Roles.CLOSED:
                return Response({"error": "Conversation is closed"}, status=400)

            if Message.objects.filter(id=msg_id).exists():
                return Response({"error": "Message already exists"}, status=status.HTTP_400_BAD_REQUEST)
            Message.objects.create(
                started_at=timestamp,
                id=msg_id,
                conversation=conversation,
                content=data["content"],
                type=data["direction"]
            )
            return Response(status=status.HTTP_201_CREATED)
        
        if type_ == "CLOSE_CONVERSATION":
            conv_id = data["id"]
            conversation = Conversation.objects.filter(id=conv_id).first()
            if not conversation:
                return Response({"error": "Conversation not found"}, status=404)
            conversation.state = Conversation.Roles.CLOSED
            conversation.closed_at = timestamp
            conversation.save()
            return Response(status=status.HTTP_200_OK)
        
class ConversationDetailView(RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    lookup_field = 'id'