# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from messenger.models import *

class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']
        recipient_id = text_data_json['recipient_id']

        recipient = Users.objects.get(id=recipient_id)
        message = Messages.objects.create(sender=self.scope['user'], destinate=recipient, text=message_text)
        message.save()

        if recipient.is_online:
            async_to_sync(self.channel_layer.group_send)(
                f"chat_{recipient_id}",
                {
                    'type': 'chat_message',
                    'message': message_text
                }
            )

        
    def chat_message(self, event):
        message = event['message']
        
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))
