
from django.conf.urls import include, url
from django.contrib import admin

from aesthetic_computation.views import home, post, arxiv, aasjobmap

urlpatterns = [
    # index
    url(r'^$', home, name='home'),

    # single post
    url(r'^(?P<id>[0-9]+)/$', post, name='post'),

    # arxiv scraper
    url(r'^arxiv707/$', arxiv, name='arxiv'),
    url(r'^arxiv707/(?P<date>[A-Za-z0-9\-]+)/$', arxiv, name='arxiv'),

    # admin
    url(r'^admin707/', admin.site.urls),

    # aas job map
    url(r'^aasjobmap/', aasjobmap, name='aasjobmap'),

    # category listing (must come last)
    url(r'^(?P<category_name>[A-Za-z0-9&\-]+)/', home, name='category'),
]

handler404 = '.views.handler404'
handler500 = '.views.handler500'
