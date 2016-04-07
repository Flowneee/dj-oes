from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^subject/new/$',views.subject_new, name='subject_new'),
	url(r'^question/new/$',views.question_new, name='question_new'),
	url(r'^answer/new/$',views.answer_new, name='answer_new'),
]