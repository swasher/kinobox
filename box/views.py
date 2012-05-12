#!/usr/bin/env python
#coding: utf-8

# Create your views here

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from box.models import *
from lib import tmdb_addon
from lib.functions import *
from django.utils import simplejson
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def add(request):
    return render_to_response('add_form.html')

def about(request):
    return render_to_response('about.html')

def grid(request):
    #типа так можно сделать фильмтрацию
    #films_list=Movi.objects.filter(title__icontains='зв')

    #if 'genr' in request.GET and request.GET['genr']:
    #    genr = unicode(request.GET['genr'])

    year=0
    if 'year' in request.GET and request.GET['year']:
        year = unicode(request.GET['year'])


    films_list=Movi.objects.all()
    if year:
        films_list=Movi.objects.filter(year=year)



    paginator = Paginator(films_list, 3) # Show 3 movie per page

    page = request.GET.get('page')
    try:
        page=int(page)
    except (TypeError, ValueError):
        page=1

    try:
        films = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        films = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        films = paginator.page(paginator.num_pages)

    return render_to_response('grid.html', {'results': films, 'year': year})



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

def moviepage(request, idd):
    idd=safe_int(idd)
    # todo взять трейлер с TMDB
    m=Movi.objects.get(tmdb_id=idd)
    return render_to_response('moviepage.html', {'movi': m})

def personpage(request, idd):
    idd=safe_int(idd)
    p=Person.objects.get(tmdb_id=idd)
    return render_to_response('personpage.html', {'pers': p})

def moviedel(request, id):
    id=safe_int(id)
    m=Movi.objects.get(tmdb_id=id)
    m.delete()
    return redirect('/grid/')

def change_starred_ajax(request):
    results = {'success':False}
    if request.method == u'GET':
        GET = request.GET
        if GET.has_key(u'pers'):
            pers_id = int(GET[u'pers'])
            person=Person.objects.get(tmdb_id=pers_id)
            person.starred=not person.starred
            person.save()
            results = {'success':True}
            results.update({'starstatus':person.starred})
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def change_seen_ajax(request):
    results = {'success':False}
    if request.method == u'GET':
        GET = request.GET
        if GET.has_key(u'mov'):
            movi_id = int(GET[u'mov'])
            m=Movi.objects.get(tmdb_id=movi_id)
            m.seen=not m.seen
            m.save()
            results = {'success':True}
            results.update({'seenstatus':m.seen})
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def change_stored_ajax(request):
    results = {'success':False}
    if request.method == u'GET':
        GET = request.GET
        if GET.has_key(u'mov'):
            movi_id = int(GET[u'mov'])
            m=Movi.objects.get(tmdb_id=movi_id)
            m.stored=not m.stored
            m.save()
            results = {'success':True}
            results.update({'storedstatus':m.stored})
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')