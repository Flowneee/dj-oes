from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
#    url(r'^login',
#        RedirectView.as_view(url='',
#                             query_string=True)),
    url(r'^', include(admin.site.urls)),

]
