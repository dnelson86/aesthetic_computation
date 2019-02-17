
from django.conf.urls import include, url
from django.contrib import admin

from .views import home, post

urlpatterns = [
    # index
    url(r'^$', home, name='home'),

    # single post
    url(r'^(?P<id>[0-9]+)/$', post, name='post'),

    # category listing (must come after post)
    url(r'^(?P<category>[A-Za-z0-9]+)/', home, name='category'),

    # admin
    url(r'^admin/', admin.site.urls),
]

handler404 = '.views.handler404'
handler500 = '.views.handler500'
