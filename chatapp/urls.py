from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.authtoken.views import obtain_auth_token


router=DefaultRouter()
router.register('users',UserView)
router.register('profile',ProfileView)

urlpatterns = [
    path('auth/',obtain_auth_token),
    path('',include(router.urls)),
    path('userprofile/<str:username>',GetProfileFromUser.as_view()),
    path('friends/<int:user_id>',NonFriendsUserView.as_view()),
    path('friendrequestsent/<str:boolname>',FriendRequestSentView.as_view()),
    path('friendrequestreceive/<int:profile_id>',FriendRequestReceive.as_view()),
    path('friendrequestreceiveconfirm/<str:confirmbool>',FriendRequestReceiveConfirm.as_view()),
    path('userfriends/<int:prof_id>',ProfileFrnds.as_view()),
    path('chatmessages',MessagesView.as_view()),
    path('postmessage',PostMessage.as_view()),
    path('remove_status/<int:logout_id>',Remove_online_status.as_view()),
    path('delete_user/<int:del_id>',del_user.as_view())
]
