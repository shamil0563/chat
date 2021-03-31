from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus import DatePickerInput
from .models import *
from datetime import date
from django.forms.widgets import DateInput
from django.shortcuts import get_object_or_404
import sys
sys.path.append('..')
from chat.miniChat.settings import *


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Aдpec Электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль еще раз')

    birth_date = forms.DateField(input_formats=DATE_INPUT_FORMATS, widget=DatePickerInput(format='%d-%m-%Y'))

    def clean_password1(self):
        password1 = self.cleaned_data['password1']

        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()

        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',
                  'address', 'birth_date', 'image',)


class ChangeUserInfoForm(forms.ModelForm):
    birth_date = forms.DateField(input_formats=DATE_INPUT_FORMATS, widget=DatePickerInput(format='%d-%m-%Y'))

    class Meta:
        model = AdvUser
        fields = ('username', 'first_name', 'last_name', 'email', 'address', 'birth_date', 'image',)


class UserSearchForm(forms.Form):
    keyword = forms.CharField(required=False, label='', max_length=50)
