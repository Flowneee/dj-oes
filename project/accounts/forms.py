# coding: utf-8

from django.contrib.auth import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.fields import BooleanField

from .models import User


class UserCreationForm(forms.UserCreationForm):

    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args, **kargs)

    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'patronymic')


class UserChangeForm(forms.UserChangeForm):

    def __init__(self, *args, **kargs):
        super(UserChangeForm, self).__init__(*args, **kargs)

    is_superuser = BooleanField(
        label=_('Суперпользователь'),
        help_text=_('Является суперпользователем'),
        initial=False, required=False
    )

    class Meta:
        model = User
        fields = '__all__'
