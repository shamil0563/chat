from rest_framework import serializers
from .models import AdvUser


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdvUser
        fields = ('pk', 'username', 'email', 'first_name', 'last_name')
