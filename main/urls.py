from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import *
app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about', AboutView.as_view(), name='about'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/profile/', IndexView.as_view(), name='profile'),
    path('accounts/friends/request/confirm/<str:slug>/', request_confirm, name='request_confirm'),
    path('account/logout/', LogoutView.as_view(next_page="/accounts/login/"), name='logout'),
    path('account/register/', RegisterView.as_view(), name='register'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/friends/', FriendView.as_view(), name='friends_user'),
    path('accounts/friends/delete/<str:slug>/', DeleteFriendView.as_view(), name='delete_friend'),
    path('accounts/friends/request/', FriendRequestView.as_view(), name='request_friend'),
    path('accounts/friends/list/', by_user_processor, name='list_user'),
    path('accounts/friends/list/<str:slug>', add_friend2, name='add_friend2'),
    path('api/users/', api_user),
]