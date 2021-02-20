from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .serializers import *
from django.db.models import Q
from django.contrib import messages
import logging

def api_user(request):
    if request.method == 'GET':
        users = AdvUser.objects.all()
        serializer = UserSerializers(users, many=True)
        return JsonResponse(serializer.data, safe=False)


class FriendListView(TemplateView):
    template_name = 'main/search_user.html'


class IndexView(TemplateView):
    template_name = 'main/index.html'


class UserLoginView(LoginView):
    template_name = 'main/login.html'


def by_user_processor(request):
    usersadd = AdvUser.objects.exclude(pk=request.user.pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(username__icontains=keyword)
        usersadd = usersadd.filter(q)
    else:
        keyword = ''
    form = UserSearchForm(initial={'keyword': keyword})
    friends = Friend.objects.filter(user=request.user).values_list('friend', flat=True)
    context = {'usersadd': usersadd, 'friends': friends, 'form': form}

    return render(request, 'main/search_user.html', context)


class AboutView(TemplateView):
    template_name = 'main/about.html'


def add_friend2(request, slug):
    friend = Friend()
    friend.user = request.user
    friend.friend = AdvUser.objects.get(username=slug)
    friend.slug = friend.user.username + 'and' + friend.friend.username
    friend2 = Friend()
    friend2.friend = request.user
    friend2.user = AdvUser.objects.get(username=slug)
    friend2.slug = friend2.user.username + 'and' + friend2.friend.username
    friend.is_friend = True
    friend2.is_friend = True
    friend.sender = request.user
    friend2.sender = request.user
    friend.save()
    friend2.save()
    messages.add_message(request, messages.SUCCESS, 'Запрос на дружбу пользователю ' + friend.friend.username
                         + ' отправлен')
    return HttpResponseRedirect(reverse('main:list_user'))


def request_confirm(request, slug):
    friend1 = Friend.objects.get(user=request.user, slug=slug)
    friend2 = Friend.objects.get(friend=request.user, slug=friend1.friend.username + 'and' + request.user.username)
    friend1.add_friend = True
    friend2.add_friend = True
    friend2.save()
    friend1.save()
    messages.add_message(request, messages.SUCCESS, 'Пользователь добавлен в друзья')
    return HttpResponseRedirect(reverse('main:request_friend'))


class RegisterView(SuccessMessageMixin, CreateView):
    model = AdvUser
    template_name = 'main/register.html'
    success_message = 'Вы зарегистрированы!'
    form_class = RegistrationForm
    success_url = reverse_lazy('main:index')


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:index')
    success_message = 'Личные данные пользователя изменены'

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.request.user.id)


class DeleteFriendView(DeleteView):
    model = Friend
    template_name = 'main/profile_friends_delete.html'
    success_url = reverse_lazy('main:request_friend')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        friend = Friend.objects.get(slug=request.user.username + 'and' + self.object.friend.username)
        friend.delete()
        friend2 = Friend.objects.get(slug=self.object.friend.username + 'and' + request.user.username)
        friend2.delete()
        return HttpResponseRedirect(success_url)


class FriendRequestView(LoginRequiredMixin, ListView):
    model = Friend
    template_name = 'main/request_friend.html'
    context_object_name = 'friends'

    def get_queryset(self):
        queryset = Friend.objects.filter(user=self.request.user.pk, add_friend=False)
        return queryset


class FriendView(LoginRequiredMixin, ListView):
    model = Friend
    template_name = 'main/friends.html'
    context_object_name = 'friends'

    def get_queryset(self):
        queryset = Friend.objects.filter(user=self.request.user.pk, add_friend=True)
        return queryset
