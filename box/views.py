#!/usr/bin/env python
#coding: utf-8

# Create your views here

from django.http import HttpResponse
from django.shortcuts import render_to_response
from box.models import *
import lib.tmdb
from lib import tmdb_addon
from tmdb import *
from lib.functions import *
import lib.tmdb
import datetime


def add(request):
    return render_to_response('add_form.html')

def grid(request):
    q=Movi.objects.all()
    return render_to_response('grid.html', {'results': q})

def changeseen(request, idd):
    #изменяет флаг seen на противоположный
    #request содержит id который надо изменить
    #blabla
    idd=safe_int(idd)
    mov=Movi.objects.filter(tmdb_id=idd)[0]
    a=mov.seen
    mov.seen=not a
    mov.save()
    q=Movi.objects.all()
    return render_to_response('grid.html', {'results': q})

def searchresult(request):
    """Функция get_list_by_name('zapros') возвращает объект:
        mov.id - tmdb id
        mov.title - title
        mov.year - год релиза
        mov.overview - содержание
        mov.url - url на источник скрепера (tmdb)
        mov.altname - альтернативное название
        mov.origname - оригинальное название
        mov.poster - линк на постер

        Для другого источника можно написать плагин и вызвать как kinopoisk_addon.getlist_by_name(q)"""
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        #q=q.decode('utf8')
        q=unicode(q)
        results=tmdb_addon.get_list_by_name(q)
        return render_to_response('search_result.html', {'zapros': q, 'results': results})
    else:
        return HttpResponse('Введите поисковый запрос.')

def doadd(request):
    if 'id' in request.GET and request.GET['id']:
        id = request.GET['id']
    id=safe_int(id)
    if Movi.objects.filter(tmdb_id=id):
        return HttpResponse('Фильм уже в базе')
    else:
        searchResult=lib.tmdb.getMovieInfo(id)

        #get poster
        try:
            poster=searchResult['images'][0]['w154']
        except:
            poster=''

        #get one string with countries
        countries_list=[]
        for country in searchResult['countries']: countries_list.append((searchResult['countries'][country]).keys()[0])
        countries_list=", ".join(countries_list)

        #get genre list
        genre_list=[]
        genres=searchResult['categories']['genre'].keys()
        for genre in genres: genre_list.append(genre)
        #genre_list=", ".join(genre_list)

        mov=Movi(title=searchResult['name'],
            overview=searchResult['overview'],
            origtitle = searchResult['alternative_name'],
            tmdb_id=searchResult['id'],
            year = searchResult['released'][0:4],
                seen = False,
                seendate = datetime.date.today(),
                myrating = 0,
                poster = poster,
                countries=countries_list,)
        mov.save()

        for genre in genre_list:
            try:
                gen=Genre.objects.filter(genre=genre)[0]
            except:
                g=Genre(genre=genre)
                g.save()
            gen=Genre.objects.filter(genre=genre)[0]
            mov.genres.add(gen)
            mov.save()
        q=Movi.objects.all()
        return render_to_response('grid.html', {'results': q})


