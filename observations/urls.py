from django.conf.urls import patterns, url

from observations import views

urlpatterns = patterns('',
    # eg: /aat/2013/5/27/
    url(r'^(?P<name>.+?)/(?P<year>\d{4})/(?P<month>\d{1,2})/'
        r'(?P<day>\d{1,2})/$', 
        views.night, name='night'),
    # eg: /aat/2013/5/
    url(r'^(?P<name>.+?)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 
        views.month, name='month'),
    # eg: /aat/2013/
    url(r'^(?P<name>.+?)/(?P<year>\d{4})/$', 
        views.year, name='year'),
    # eg: /aat/
    url(r'^(?P<name>.+?)/$', 
        views.telescope, name='telescope'),
)

