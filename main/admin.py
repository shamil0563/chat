from django.contrib import admin
from .models import AdvUser, Friend, Message, ChatGroup

admin.site.register(AdvUser)
admin.site.register(Friend)
admin.site.register(Message)
admin.site.register(ChatGroup)
