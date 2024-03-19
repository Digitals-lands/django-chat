import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import  Users

class online(WebsocketConsumer):
    
    # Dictionnaire pour stocker les utilisateurs en ligne
    online_users = {}  

    def connect(self):
        # Ajout de l'utilisateur au groupe_name 'online'
        self.room_group_name = 'online'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name 
        )
        # Ajout de l'utilisateur au dictionnaire des utilisateurs en ligne
        user = self.scope['user']
        self.online_users[user.id] = user
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
                {
                    'type':'update_online_users', 
                }
        )
        self.accept()

    def disconnect(self, close_code):
        
        user_id = self.scope['user'].id
        
        #Condition pour retirer l'utilisateur au dictionnaire des utilisateurs en ligne
        if user_id in self.online_users:
            del self.online_users[user_id]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
                {
                    'type':'update_online_users',
                    
                }
        )
        
    def receive(self,text):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
                {
                    'type':'update_online_users',
                    
                }
        )

    # Fonction d'envoie des utilisateurs en ligne
    def update_online_users(self,event):
        user_info = []
        all_users = Users.objects.all()
        
        
        for user in all_users:
            if user.id in self.online_users: 
                user_info.append({'username': user.username, 'adresse':user.adresse, 'id': str(user.id), 'online': True})
            else:
                user_info.append({'username': user.username, 'adresse':user.adresse,'id': str(user.id), 'online': False})
      
        self.send(text_data=json.dumps({
            'type':'online',
            'users': user_info,
            
        }))
        
        