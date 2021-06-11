from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import *

app_name = 'main'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about', AboutView.as_view(), name='about'),
    path('account/messages/<int:pk>', correspondence, name='private_message'),
    path('account/messages/', ListCorrespondenceView.as_view(), name='messages'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/profile/', IndexView.as_view(), name='profile'),
    path('account/logout/', LogoutView.as_view(next_page="/accounts/login/"), name='logout'),
    path('account/register/', RegisterView.as_view(), name='register'),
    path('account/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('account/friends/delete/<str:slug>/', DeleteFriendView.as_view(), name='delete_friend'),
    path('account/friends/request/<str:slug>/', request_confirm, name='request_confirm'),
    path('account/friends/request/', FriendRequestView.as_view(), name='request_friend'),
    path('account/friends/', FriendView.as_view(), name='friends_user'),
    path('users/list/', by_user_processor, name='list_user'),
    path('users/list/<str:slug>', add_friend2, name='add_friend2'),
    path('room/<str:slug>', message, name='message'),
]
