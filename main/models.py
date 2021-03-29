from django.db import models
from .utilities import get_timestamp_path
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group


class AdvUser(AbstractUser):
    class Meta:
        db_table = 'AdvUser'

    address = models.TextField(blank=True, db_index=True, verbose_name='Адрес')
    birth_date = models.DateField(blank=True, null=True)
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Аватарка')


class Friend(models.Model):
    class Meta:
        db_table = 'Friend'
    sender = models.ForeignKey(AdvUser, related_name='sender', on_delete=models.CASCADE)
    is_friend = models.BooleanField(default=False, verbose_name='Запрос отправлен?')
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE)
    friend = models.ForeignKey(AdvUser, related_name='friends', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    add_friend = models.BooleanField(default=False, verbose_name='Добавить в друзья?')


class Message(models.Model):
    class Meta:
        db_table = 'Message'
    text = models.CharField(max_length=255)
    group = models.ForeignKey('ChatGroup', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class ChatGroup(Group):
    class Meta:
        db_table = 'ChatGroup'
    description = models.TextField(blank=True, help_text="description of the group")
    mute_notifications = models.BooleanField(default=False, help_text="disable notification if true")
    icon = models.ImageField(help_text="Group icon", blank=True, upload_to="chartgroup")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    user1 = models.ForeignKey(AdvUser, related_name='recipient', on_delete=models.CASCADE)
    user2 = models.ForeignKey(AdvUser, related_name='message_sender', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return '/room/%s' % self.slug
