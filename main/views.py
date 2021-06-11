from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404, HttpResponse
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render


class FriendListView(TemplateView):
    """Поиск пользователей"""
    template_name = 'main/search_user.html'


class IndexView(TemplateView):
    """Главная страница"""
    template_name = 'main/index.html'


class UserLoginView(LoginView):
    """Страница входа"""
    template_name = 'main/login.html'


def by_user_processor(request):
    """Api User"""
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
    """О нас"""
    template_name = 'main/about.html'


def add_friend2(request, slug):
    """Добавление в друзья"""
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
    """Подтверждение запроса в друзья"""
    friend1 = Friend.objects.get(user=request.user, slug=slug)
    friend2 = Friend.objects.get(friend=request.user, slug=friend1.friend.username + 'and' + request.user.username)
    friend1.add_friend = True
    friend2.add_friend = True
    friend2.save()
    friend1.save()
    messages.add_message(request, messages.SUCCESS, 'Пользователь добавлен в друзья')
    return HttpResponseRedirect(reverse('main:request_friend'))


class RegisterView(SuccessMessageMixin, CreateView):
    """Подтверждение регистрации"""
    model = AdvUser
    template_name = 'main/register.html'
    success_message = 'Вы зарегистрированы!'
    form_class = RegistrationForm
    success_url = reverse_lazy('main:index')


@login_required()
def message(request, slug):
    """Чат комната"""
    if ChatGroup.objects.get(slug=slug):
        chatgroup = ChatGroup.objects.get(slug=slug)
        if request.user.username not in chatgroup.slug:
            return HttpResponse(":)")
        if Message.objects.filter(group=chatgroup).exists():
            chat_message = Message.objects.filter(group=chatgroup)
            not_read_chat_message = Message.objects.filter
            return render(request, 'main/message.html', {'chatgroup': chatgroup, 'chat_message': chat_message})
        else:
            return render(request, 'main/message.html', {'chatgroup': chatgroup})


class ListCorrespondenceView(LoginRequiredMixin, ListView):
    model = ChatGroup
    template_name = 'main/list_correspondence.html'
    context_object_name = 'correspondences'

    def get_queryset(self):
        if ChatGroup.objects.filter(slug__startswith=self.request.user.username).exists():
            queryset = ChatGroup.objects.filter(slug__startswith=self.request.user.username)

            return queryset
        elif ChatGroup.objects.filter(slug__endswith=self.request.user.username).exists():
            queryset = ChatGroup.objects.filter(slug__endswith=self.request.user.username)
            return queryset


@login_required()
def correspondence(request, pk):

    usr_msg = AdvUser.objects.get(pk=pk)
    slug1 = request.user.username + 'and' + usr_msg.username
    slug2 = usr_msg.username + 'and' + request.user.username
    if ChatGroup.objects.filter(slug=slug1).exists():

        return HttpResponseRedirect(reverse('main:message', args=[slug1]))
    elif ChatGroup.objects.filter(slug=slug2).exists():
        return HttpResponseRedirect(reverse('main:message', args=[slug2]))
    else:
        ChatGroup.objects.create(slug=slug1, name=slug1, description=slug1, user1=request.user, user2=usr_msg)
        return HttpResponseRedirect(reverse('main:message', args=[slug1]))


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Изменение данных пользователей"""
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
    """Удаление друга"""
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
    """Список запросов в друзья"""
    model = Friend
    template_name = 'main/request_friend.html'
    context_object_name = 'friends'

    def get_queryset(self):
        queryset = Friend.objects.filter(user=self.request.user.pk, add_friend=False)
        return queryset


class FriendView(LoginRequiredMixin, ListView):
    """Список друзей"""
    model = Friend
    template_name = 'main/friends.html'
    context_object_name = 'friends'

    def get_queryset(self):
        queryset = Friend.objects.filter(user=self.request.user.pk, add_friend=True)
        return queryset
