from django.conf.urls import patterns, include, url
from django.conf import settings

import observations.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'astrowatch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^observations/', 
        include('observations.urls', namespace='observations')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/signup/$', observations.views.SignupView.as_view(),
        name="account_signup"),
    url(r'^account/', include('account.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
         'document_root': settings.MEDIA_ROOT}))
