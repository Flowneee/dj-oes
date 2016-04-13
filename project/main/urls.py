from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^subject/new/$', views.SubjectCreateView.as_view(),
        name='subject_new'),
    url(r'^question/new/$', views.QuestionCreateView.as_view(),
        name='question_new'),
    url(r'^answer/new/$', views.AnswerCreateView.as_view(), name='answer_new'),
    url(r'^subject/$', views.SubjectListView.as_view(), name='subject_list'),
    url(r'^question/$', views.QuestionListView.as_view(),
        name='question_list'),
    url(r'^answer/$', views.AnswerListView.as_view(), name='answer_list'),
    url(r'^subject/(?P<subject_id>[0-9]+)/$', views.SubjectView,
        name='subject_detail'),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.QuestionView,
        name='question_detail'),
    url(r'^answer/(?P<answer_id>[0-9]+)/$', views.AnswerView,
        name='answer_detail'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^upload_csv/$', views.UploadCsvView.as_view(), name='upload_csv'),
    url(r'^$', views.index_view, name='index'),
]
