from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='tutor'),
    url(r'^test/new/$', views.TestCreateView.as_view(),
        name='test_new'),
    url(r'^test/(?P<test_id>[0-9]+)/$', views.TestView,
        name='test_detail'),
    url(r'^subject/(?P<subject_id>[0-9]+)', views.TestListView,
        name='test_list'),
    url(r'^subject/', views.SubjectView.as_view(), name='tutor_subject_list'),
]
