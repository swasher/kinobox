#coding: utf-8

from django.conf.urls.defaults import patterns, include, url
from kinobox.box.views import add, grid, searchresult, doadd, personpage, moviepage, moviedel, change_starred_ajax, change_seen_ajax, change_stored_ajax, about
from django.conf import settings

# deprecated from django.conf.urls.defaults import *

#MAIN TO DO
#todo - удаление фильма в виде функции класса movi.delete(id)
#todo - вынести добавление фильма с TMDB в функцию
#todo - в моделях используется прямой линк url='/static/nobody.jpg', разрешить как-то
#todo - ЛИНКИ жанры, алфавит, годы

#todo - COMPLETE pagination для grid-a

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
    (r'^$', grid),     #главный список
    (r'^add/$', add),       #добавляем фильмы
    (r'^searchresult/$', searchresult),       #что нашлось
    (r'^moviedel/(?P<id>\d+)/$', moviedel),
    (r'^doadd/$', doadd),       #выполнить вставку в базу выбранного фильма
    (r'^about/$', about),     #about
    (r'^grid/$', grid),     #главный список
    (r'^grid/(?P<page>\d+)/(?P<year>\d{4})/$', grid),     #главный список
    (r'^personpage/(?P<idd>\d+)/$', personpage),     #подробности персоны
    (r'^moviepage/(?P<idd>\d+)/$', moviepage),     #подробности фильма
    (r'^change_seen_ajax/$', change_seen_ajax),
    (r'^change_stored_ajax/$', change_stored_ajax),
    (r'^change_starred_ajax/$', change_starred_ajax),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )


