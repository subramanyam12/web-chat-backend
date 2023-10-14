from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,related_name='profiles', on_delete=models.CASCADE)
    username=models.CharField(max_length=100,blank=True,null=True)
    usertag=models.CharField(max_length=100,blank=True,null=True)
    profile_img=models.ImageField(upload_to='images',blank=True,null=True)
    friends=models.ManyToManyField(User,blank=True)
    friendsrequest_sent=models.ManyToManyField(User,related_name='friendsrequest_sent',blank=True)
    friendsrequest_receive=models.ManyToManyField(User,related_name='friendsrequest_receive',blank=True)
    online_status=models.BooleanField(default=False)
    last_seen=models.DateTimeField(default=datetime.now())
    def __str__(self):
        return self.username if self.username else str(self.user)
    
    
class ChatMessages(models.Model):
    body=models.TextField()
    sender_profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='sender_profile')
    receiver_profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='receiver_profile')
    time_now=models.DateTimeField(default=datetime.now())
  
    def __str__(self):
        return f'{self.sender_profile} is sent Message to {self.receiver_profile}'



