from django.shortcuts import render, redirect
from messenger.models import *
from django.contrib.auth import login,logout
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q,Subquery
import django
from datetime import datetime, timedelta
import string
import secrets
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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

@login_required
def chat_messages(request,id):
     message = Messages.objects.filter(Q(sender_id=request.user.id, destinate_id=id) | Q(sender_id=id, destinate_id=request.user.id)).order_by('created_at')[:50]
     if message:
          formatted_messages = []
          for messag in message:
               messag.confirmation_lecture =True
               messag.save()
               formatted_message = {
                    'id': str(messag.id),
                    'text': messag.text,
                    'file': messag.file.url,
                    'created_at': format_date(messag.created_at),
                    'sender':messag.sender.id,
                    'destinate':messag.destinate.id,
                    'username':messag.sender.username,
                    'photo':messag.sender.photo.url,

                    }
               formatted_messages.append(formatted_message)
                    

          return django.http.JsonResponse({'messages': formatted_messages,})
     else:
          return django.http.JsonResponse({'messages': None, })

def format_date(created_at):
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    if created_at.date() == today.date():
        return "aujourd'hui à " + created_at.strftime("%H:%M")
    elif created_at.date() == yesterday.date():
        return "hier à " + created_at.strftime("%H:%M")
    else:
        return created_at.strftime("%d %B à %Hh%M")

    
