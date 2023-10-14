from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import datetime

# Create your views here.
class UserView(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    authentication_classes=[TokenAuthentication]
    

class ProfileView(viewsets.ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer  

class GetProfileFromUser(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            username = self.kwargs.get('username')
            user = User.objects.get(username=username)
            userprofile = Profile.objects.get(user=user)
            userprofile.online_status=True
            userprofile.save()
            return userprofile
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        except Profile.DoesNotExist:
            raise serializers.ValidationError("UserProfile does not exist.")


class NonFriendsUserView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)

        except User.DoesNotExist: 
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.get(id=user_id)
        userprofile = Profile.objects.get(user=user)
        # userprofile=user.profiles
        prof_frnds=userprofile.friends.all()
        # sugg_frnds=User.objects.exclude(id__in=prof_frnds).exclude(profiles=userprofile)
        profiles=Profile.objects.exclude(user__in=prof_frnds).exclude(id=userprofile.id)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FriendRequestSentView(APIView):
    def post(self,request,boolname):
        sender=User.objects.get(pk=request.POST['sender'])
        receiver=User.objects.get(pk=request.POST['receiver'])
        sender_prof=Profile.objects.get(user=sender)
        received_profile=Profile.objects.get(user=receiver)
        if boolname=='add':
            sender_prof.friendsrequest_sent.add(receiver)
            received_profile.friendsrequest_receive.add(sender)
        else:
            sender_prof.friendsrequest_sent.remove(receiver)
            received_profile.friendsrequest_receive.remove(sender)
        sender_prof.save()
        received_profile.save()
        
        return Response({'requestsentto' if boolname=='add' else 'requestcancelled':request.POST['receiver']}, status=status.HTTP_200_OK)


class FriendRequestReceive(APIView):
    def get(self,request,profile_id): 
        prof=Profile.objects.get(id=profile_id)
        reqreceive=Profile.objects.filter(user__in=[*prof.friendsrequest_receive.all()])
        serializer=ProfileSerializer(reqreceive,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   
    

class FriendRequestReceiveConfirm(APIView):
    def post(self,request,confirmbool):
        sender=User.objects.get(pk=request.POST['sender'])
        receiver=User.objects.get(pk=request.POST['receiver'])
        sendprof=Profile.objects.get(user=sender)
        recevprof=Profile.objects.get(user=receiver)

        if confirmbool=='confirm':
            sendprof.friends.add(receiver)
            sendprof.friendsrequest_receive.remove(receiver)
            sendprof.save()

            recevprof.friends.add(sender)
            recevprof.friendsrequest_sent.remove(sender)
            recevprof.save()
        else:
            sendprof.friendsrequest_receive.remove(receiver)
            sendprof.save()
            recevprof.friendsrequest_sent.remove(sender)
            recevprof.save()
            
        return Response({'Accepted ' if confirmbool=='confirm' else 'Cancelled' }, status=status.HTTP_200_OK)
        

class ProfileFrnds(APIView):
    def get(self,request,prof_id):
        send_prof=Profile.objects.get(id=prof_id)
        frnds=send_prof.friends.all()
        frndprofies=Profile.objects.filter(user__in=frnds)
        serializer=FreindsSerializer(frndprofies,many=True)
        messages=ChatMessages.objects.filter(receiver_profile=send_prof,sender_profile__in=frndprofies ).values()
         
        for i in serializer.data:
            lm=''
            tm=''
            for j in messages:
                if i['id']==j['sender_profile_id']:
                    lm=j['body']
                    tm=j['time_now']
            i['last_message']=lm
            i['msg_time']=tm
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessagesView(APIView):
    def get(self,request):
        messages=ChatMessages.objects.all()
        serializers=MessagesSerializer(messages,many=True)
        return Response(serializers.data)

class PostMessage(APIView):
    def post(self,request):
        body=request.POST['body']
        sender=Profile.objects.get(id=request.POST['sender'])
        receiver=Profile.objects.get(id=request.POST['receiver'])
        chatmsg=ChatMessages.objects.create(body=body,sender_profile=sender,receiver_profile=receiver)
        chatmsg.save()
        serializers=MessagesSerializer(chatmsg)
        return Response(serializers.data)

class Remove_online_status(APIView):
    def post(self,request,logout_id):
        profile=Profile.objects.get(id=logout_id)
        profile.online_status=False
        profile.last_seen=datetime.now()
        profile.save()
        return Response({'status': 'Logged out'})
     
class del_user(APIView):
    def post(self,request,del_id):
        del_user=User.objects.get(id=del_id)
        del_user.delete()
        return Response({'msg':'deleted'})

