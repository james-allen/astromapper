from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'astrowatch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^observations/', 
        include('observations.urls', namespace='observations')),
    url(r'^admin/', include(admin.site.urls)),
)
