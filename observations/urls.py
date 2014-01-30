from django.conf.urls import patterns, url

from observations import views

urlpatterns = patterns('',
    url(r'^data/$', views.getdata, name='getdata'),
    url(r'^user/(?P<username>.+?)/$',
        views.user_view, name='user'),
    # eg: /aat/2013/5/27/
    url(r'^(?P<name>.+?)/(?P<year>\d{4})/(?P<month>\d{1,2})/'
        r'(?P<day>\d{1,2})/$', 
        views.night_view, name='night'),
    # eg: /aat/2013/5/
    url(r'^(?P<name>.+?)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 
        views.month_view, name='month'),
    # eg: /aat/2013/
    url(r'^(?P<name>.+?)/(?P<year>\d{4})/$', 
        views.year_view, name='year'),
    # eg: /aat/
    url(r'^(?P<name>.+?)/$', 
        views.telescope_view, name='telescope'),
)
