from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^subject/new/$', views.subject_new_view, name='subject_new'),
    url(r'^question/new/$', views.question_new_view, name='question_new'),
    url(r'^answer/new/$', views.answer_new_view, name='answer_new'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
]
