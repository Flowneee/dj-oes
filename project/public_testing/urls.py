from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^main/$', views.MainPublicTestingView.as_view(),
        name='public_testing_main'),
    url(r'^test/$', views.PublicTestView.as_view(),
        name='public_test'),
    url(r'^ajax_get_public_question/$',
        views.AJAXGetPublicQuestionView.as_view(),
        name='ajax_get_question'),
    url(r'^ajax_answer_public_question/$',
        views.AJAXAnswerPublicQuestionView.as_view(),
        name='ajax_answer_public_question')
]
