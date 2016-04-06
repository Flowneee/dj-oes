from django.contrib import admin
from django.contrib.auth import admin as aauth
from django.contrib.auth.models import Group

from users.models import User, ProxyGroup

# Register your models here.

admin.site.register(User)
admin.site.unregister(Group)
admin.site.register(ProxyGroup, aauth.GroupAdmin)
