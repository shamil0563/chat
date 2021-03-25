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

    class Meta(AbstractUser.Meta):
        pass


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
    text = models.CharField(max_length=255)
# Create your models here.
