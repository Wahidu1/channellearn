import json
from rest_framework.views import APIView
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class SendNotificationAPIView(APIView):
    def post(self, request):
        message = request.data.get('message', 'No message')

        # channel
        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': message,
            }
        )
        return Response({"status": "sent", "message": message})

