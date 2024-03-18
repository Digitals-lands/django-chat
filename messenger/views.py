from django.shortcuts import render, redirect
from messenger.models import *
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.

def register(request):
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
               photo=photo
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
          return render(request, 'chat.html')
     else:
          return redirect('register')

def login_user(request):
    return render(request, 'login.html')
