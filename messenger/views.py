from django.shortcuts import render, redirect
from messenger.models import *
from django.contrib.auth import login,logout
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.

def register(request):
    
    if request.user.id:
        return redirect('chat')
    if request.method == "POST":
        username = request.POST.get('username')
        photo = request.FILES.get('photo')
        password = request.POST.get('password')

        if Users.objects.filter(username=username).exists():
               messages.error(request, "Cet utilisateur existe déjà.")
               return redirect('register') 

        user = Users.objects.create_user(
               username=username,
               password=password,
               photo=photo, 
               is_online=True
          )
        if user is not None:
               login(request, user)
               return redirect('chat')  
        else:
            messages.error(request, "Une erreur s'est produite lors de l'inscription. Veuillez réessayer.")
            return redirect('register') 
    else:
        return render(request, 'home.html')

def chat_message(request):
     if request.user.is_authenticated:
          users = Users.objects.exclude(id=request.user.id)
          return render(request, 'chat.html', {'users': users})
     else:
          return redirect('login')

def login_user(request):
     if request.user.id:
          return redirect('chat')
     if request.method == "POST":   
          username = request.POST.get('username')
          password = request.POST.get('password')
                    
          user = Users.objects.filter(username=username).first() 
               
          if user is not None:    
               if user.check_password(password):
                    login(request, user)  
                    user.is_online = True
                    user.save()        
                    return redirect('chat')
               else:
                    messages.error(request, "Mot de passe non valide")
          else:
               messages.error(request,"Username ou mot de passe non valide")      

     return render(request, 'login.html')
    
def deconnexion(request):
     user = request.user
     user.is_online = False
     user.save()     
     logout(request)  
     return redirect('login')


def send_message(request):
     if request.method == "POST":
          message_text = request.POST.get('message')
          receiver_username = request.POST.get('receiver_username')

          receiver = Users.objects.get(username=receiver_username)
          #print(message_text, receiver_username, receiver)
          Messages.objects.create(
               text=message_text,
               sender=request.user,
               destinate=receiver
          )
          
          channel_layer = get_channel_layer()
          async_to_sync(channel_layer.group_send)(
               f"chat_{receiver.username}",
               {
                    'type': 'chat_message',
                    'message': message_text,
                    'sender': request.user.username
               }
          )
     return redirect('chat')