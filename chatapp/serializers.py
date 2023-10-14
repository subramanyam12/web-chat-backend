from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','password']

        extra_kwargs={'password':{
            'write_only':True,
            'required':True
        }}

    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"

class FreindsSerializer(serializers.ModelSerializer):
    last_message=serializers.SerializerMethodField()
    msg_time=serializers.SerializerMethodField()
    class Meta:
        model=Profile
        fields=['id','user','username','usertag','profile_img','friends','last_message','msg_time','online_status','last_seen']
    def get_last_message(self,obj):
        return ''
    def get_msg_time(self,obj):
        return ''
    
class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChatMessages
        fields='__all__'   
        


   