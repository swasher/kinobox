#coding: utf-8

from django.conf.urls.defaults import patterns, include, url
from kinobox.box.views import add, grid, searchresult, doadd, changeseen
from django.views.static import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kinobox.views.home', name='home'),
    # url(r'^kinobox/', include('kinobox.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

urlpatterns = patterns('',
    (r'^add/$', add),       #добавляем фильмы
    (r'^searchresult/$', searchresult),       #что нашлось
    (r'^doadd/$', doadd),       #выполнить вставку в базу выбранного фильма
    (r'^grid/$', grid),     #главный список
    (r'^changeseen/(?P<idd>\d+)/$', changeseen),     #изменяет атрибут "просмотрено"
    (r'^$', grid),     #главный список
    url(r'^admin/', include(admin.site.urls)),
)