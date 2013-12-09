from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),

    url(r'^donations/accept/$', 'main.views.accept_donation', name='accept_donation'),

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/register/$', 'main.views.register', name='register'),

    url(r'^admin/', include(admin.site.urls)),
)
