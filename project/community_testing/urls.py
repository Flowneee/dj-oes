from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy

from . import views

urlpatterns = [
    url(r'^main/$', views.MainCommunityTestingView.as_view(),
        name='community_testing_main'),
    url(r'^test/$', views.CommunityTestView.as_view(),
        name='community_test'),
]
