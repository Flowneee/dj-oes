# coding: utf-8

from django.contrib import admin
from django.contrib.auth import admin as aauth
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .models import User, ProxyGroup
from .forms import UserChangeForm, UserCreationForm

# Register your models here.


class UserAdmin(aauth.UserAdmin):
    fieldsets = (
        (None, {'fields': ('full_name', 'password')}),
        (_('Персональная информация'), {'fields': (
            'email', 'last_name', 'first_name',
            'patronymic')}),
        (_('Права'), {'fields': (
            'account_level', 'is_staff', 'is_superuser',
            'groups', 'user_permissions')}),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ['full_name', 'email']

    def full_name(self, obj):
        return obj.get_full_name()
    full_name.allow_tags = True
    full_name.short_description = _('Полное имя')
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email',  'last_name', 'first_name',
                       'patronymic', 'is_active', 'is_staff', 'is_superuser'
                       'account_level', 'password1', 'password2', )}, ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'last_name', 'first_name', 'patronymic',
                    'account_level', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(ProxyGroup, aauth.GroupAdmin)
