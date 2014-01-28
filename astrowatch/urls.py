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
#    url(r'^account/signup/$', observations.views.SignupView.as_view(),
#        name="account_signup"),
#    url(r'^account/', include('account.urls')),
    url(r'accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'accounts/password_change/$', 'django.contrib.auth.views.password_change'),
    url(r'accounts/password_change_done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
         'document_root': settings.MEDIA_ROOT}))
