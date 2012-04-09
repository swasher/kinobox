#!/usr/bin/env python
#coding: utf-8

# Create your views here

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from box.models import *
from lib import tmdb_addon
from lib import tmdb
from lib.functions import *
from box.forms import SelectForm
import datetime


#from lib.tmdb import *

def add(request):
    return render_to_response('add_form.html')

def grid(request):
    #if request.method == 'POST':
    form=SelectForm(request.POST)
    q=Movi.objects.all()
    return render_to_response('grid.html', {'results': q, "form": form})
    #q=(a.year) for a in Movi.objects.all()
    #return HttpResponse(q)


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
    #return render_to_response('grid.html', {'results': q})
    return redirect('/grid/')

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
        tmdb_addon.add_tmdb_movie(id)
        return redirect('/grid/')


