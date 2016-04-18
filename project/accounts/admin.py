# coding: utf-8

from django.contrib import admin
from django.contrib.auth import admin as aauth
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .models import User, ProxyGroup
from .forms import UserChangeForm, UserCreationForm

# Register your models here.


class UserAdmin(aauth.UserAdmin):

    def full_name(self, obj):
        return obj.get_full_name()
    full_name.allow_tags = True
    full_name.short_description = _('Полное имя')
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email',  'last_name', 'first_name', 'patronymic',
                       'is_active', 'is_staff', 'is_superuser', 'account_level',
                       'study_group', 'password1', 'password2', )}, ),
    )
    fieldsets = (
        (None, {'fields': ('full_name', 'password', 'email')}),
        (_('Персональная информация'), {'fields': (
            'email', 'last_name', 'first_name',
            'patronymic', 'study_group')}),
        (_('Права'), {'fields': (
            'account_level', 'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions')}),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ['email']
        return self.readonly_fields

    readonly_fields = ['full_name']
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'last_name', 'first_name', 'patronymic',
                    'account_level', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(ProxyGroup, aauth.GroupAdmin)
