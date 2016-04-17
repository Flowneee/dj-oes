from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^main/$', views.ControlTestingListView.as_view(),
        name='control_testing_list'),
    url(r'^details_before_testing/$',
        views.ControlTestDetailsView.as_view(),
        name='control_test_details_before_testing'),
    url(r'^control_test/$', views.ControlTestView.as_view(),
        name='control_test'),
    url(r'^ajax_control_test_results/$',
        views.AJAXControlTestResultsView.as_view(),
        name='ajax_control_test_results'),
]
