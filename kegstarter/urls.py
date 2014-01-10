from django.conf.urls import patterns, include, url

from main.views import KegDetail, KegCreate, BreweryDetail, BreweryCreate

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^keg/(?P<pk>\d+)/', KegDetail.as_view(), name='keg'),
    url(r'^keg/purchase/', 'main.views.purchase', name='purchase'),
    url(r'^keg/create/', KegCreate.as_view(), name='keg_create'),
    url(r'^brewery/(?P<pk>\d+)/', BreweryDetail.as_view(), name='brewery'),
    url(r'^brewery/create/', BreweryCreate.as_view(), name='brewery_create'),
    url(r'^vote', 'main.views.vote', name='vote'),

    url(r'^donations/accept/$', 'main.views.accept_donation', name='accept_donation'),

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/register/$', 'main.views.register', name='register'),

    url(r'^admin/', include(admin.site.urls)),
)
