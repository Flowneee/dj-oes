from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^subject/new/$', views.SubjectCreateView.as_view(), name='subject_new'),
    url(r'^question/new/$', views.QuestionCreateView.as_view(), name='question_new'),
    url(r'^answer/new/$', views.AnswerCreateView.as_view(), name='answer_new'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
]
