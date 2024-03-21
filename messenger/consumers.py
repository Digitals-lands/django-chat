import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime, timedelta
from messenger.models import *

class MyConsumer(WebsocketConsumer):
    def connect(self):
        
        users = Users.objects.exclude(id=self.scope['user'].id)
        chaine1=self.scope['user'].username.lower()
        for user in users:
            chaine2 =user.username.lower()
            if chaine1<chaine2:
                self.room_groupe_name = chaine1+chaine2
            else:
                self.room_groupe_name = chaine2+chaine1
        
            async_to_sync(self.channel_layer.group_add)(
            self.room_groupe_name,
            self.channel_name
            )
        self.accept()
       
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_id =text_data_json['friends']
        receiver=Users.objects.get(id=receiver_id)
        messag=Messages.objects.create(
               text=message,
               sender=self.scope['user'],
               destinate=receiver
          )
        chaine1=self.scope['user'].username.lower()
        chaine2 =receiver.username.lower()
        if chaine1<chaine2:
            room = chaine1+chaine2
        else:
            room = chaine2+chaine1
        
        async_to_sync(self.channel_layer.group_send)(
                room,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id':str(self.scope['user'].id),
                'receiver_id':receiver_id,
                'created_at': format_date(messag.created_at),
                'sender_img':str(self.scope['user'].photo.url)
            }
        )
        def format_date(created_at):
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            if created_at.date() == today.date():
                return "aujourd'hui à " + created_at.strftime("%H:%M")
            elif created_at.date() == yesterday.date():
                return "hier à " + created_at.strftime("%H:%M")
            else:
                return created_at.strftime("%d %B à %Hh%M")

    def chat_message(self, event):
        message = event['message']
        created_at=event["created_at"]
        sender_id = event['sender_id']
        receiver_id = event['receiver_id']
        sender_img= event['sender_img']
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'sender_id':sender_id,
            'receiver_id':receiver_id,
            'sender_img':sender_img,
            'created_at':created_at,
        }))
