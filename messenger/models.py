from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone

# Create your models here.
class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.TextField()
    photo = models.ImageField(upload_to='media/photo',default='media/image_defaut/img_profils.png')
    is_online = models.BooleanField(default=False)
  
        
class Messages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(null = True)
    file = models.FileField(upload_to = 'media/document', null = True)
    sender = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='sender')
    destinate = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='destinate', null=True)
    confirmation_lecture = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
