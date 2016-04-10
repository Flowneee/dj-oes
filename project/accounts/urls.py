from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy

from . import views

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('index')}, name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]
