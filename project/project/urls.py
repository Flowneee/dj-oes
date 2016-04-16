from django.conf.urls import include, url, patterns

import main.views as mv

from . import settings


urlpatterns = [
    url(r'^$', mv.index_view, name='index'),
    url(r'^main/', include('main.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include('accounts.admin_urls')),
    url(r'^public_testing/', include('public_testing.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)), )
