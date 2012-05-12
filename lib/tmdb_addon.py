#!/usr/bin/env python
#coding: utf-8

#git clone https://github.com/dbr/themoviedb.git

import logging, urllib, datetime
from box.models import *
from django.core.files import File
from tmdb3 import set_key, get_locale, set_locale, searchMovie, set_cache, Movie

logging.basicConfig(format='%(asctime)s %(levelname)s \t %(message)s',datefmt='%d/%m/%Y %H:%M',filename='/home/swasher/kinobox/log',level=logging.DEBUG)

class kino:
    pass

def get_list_by_name(zapros):
    set_key('c97c17e619252e35bad2e158d4211fcc')
    set_locale('ru', 'ru')
    set_cache(engine='file', filename='/home/swasher/kinobox/.tmdb3cache')

    results = searchMovie(zapros)
    answer=[]
    i=0
    for movie in results[0:10]:
        mov=kino()
        #print unicode(results[i])
        searchResult = results[i]
        mov.id=searchResult.id
        mov.title=searchResult.title
        mov.year=str(searchResult.releasedate)[0:4]
        mov.overview=searchResult.overview
        mov.url='http://www.themoviedb.org/movie/'+str(mov.id)
        mov.origname=searchResult.originaltitle
        try:
            mov.altname=searchResult.alternate_titles[0].title
        except:
            mov.altname=''
        try:
            mov.poster=searchResult.poster.geturl(size='w154')
        except:
            mov.poster=''
        answer.append(mov)
        i+=1
    return answer

def add_tmdb_movie(id):
    set_key('c97c17e619252e35bad2e158d4211fcc')
    set_locale('ru', 'ru')
    set_cache(engine='file', filename='/home/swasher/kinobox/.tmdb3cache')

    m = Movi()

    try:
        mov = Movie(id)
    except:
        pass
        #обработать (не нашло фильм, или ппц ваще) sys.exc_info()[0].__dict__

    m.title=mov.title
    m.overview=mov.overview
    m.origtitle=mov.originaltitle
    m.tmdb_id=mov.id
    m.year=str(mov.releasedate)[0:4]
    m.seen=False
    m.seendate=datetime.date.today()
    m.myrating=0
    m.stored=True
    m.adddate=datetime.date.today()
    m.tagline=mov.tagline
    m.save()

    try:
        poster = urllib.urlretrieve(mov.poster.geturl(size='w92'))
        m.poster.save('poster_'+'w92_'+str(id)+'.jpg', File(open(poster[0])))
    except:
        #отсутствует постер
        #print sys.exc_info()[0].__dict__
        #{'__module__': 'tmdb3.tmdb_exceptions', '__doc__': None}
        #print 'cant retrieve'
        # если не обрабатывать - просто получается пустое поле, его можно обработать дальше
        poster = urllib.urlretrieve(mov.poster.geturl(size='w92'))
        m.poster.save('poster_'+'w92_'+str(id)+'.jpg', File(open(poster[0])))
        pass

    try:
        posterbig = urllib.urlretrieve(mov.poster.geturl(size='w500'))
        m.posterbig.save('poster_'+'w500_'+str(id)+'.jpg', File(open(posterbig[0])))
    except:
        pass

    #get counries
    countries = mov.countries
    l = ''
    for country in countries:
        if country.name=='United States of America':
            l+='USA'+', '
        else:
            l+=country.name+', '
    m.countries=l[:-2]

    genres = mov.genres
    genre_list=[]
    for genre in genres:
        genre_list.append(genre.name)

    for genre in genre_list:
        try:
            # пытаемся найти жанр по названию
            gen=Genre.objects.filter(genre=genre)[0]
        except:
            # Если не найден, возникает исключение, и мы создаем новый жанр.
            # Исключение возникает из-за попытки взять нулевой элемент пустого тупла
            g=Genre(genre=genre)
            g.save()
            gen=Genre.objects.filter(genre=genre)[0]
        m.genres.add(gen)
        m.save()

    cast=mov.cast
    for actor in cast:
        try:
            pers=Person.objects.filter(name=actor.name)[0]
        except:
            #если актера actor.name нет в базе, то вызывется исключение, актер добавляется, и обзывется как pers
            p = Person(name=actor.name, tmdb_id=actor.id)
            p.save()
            pers=Person.objects.filter(name=actor.name)[0]

            #если актера до сих пор небыло, то добавляем фото
            #todo в дальнейшем это убрать - сделать даунлоад фото, когда актер star-рится
            try:
                photo = urllib.urlretrieve(actor.profile.geturl(size='w45'))
                p.photo.save('photo_'+'w45_'+str(actor.id)+'.jpg', File(open(photo[0])))
            except:
                #отсутствует постер
                #print sys.exc_info()[0].__dict__
                #{'__module__': 'tmdb3.tmdb_exceptions', '__doc__': None}
                #print 'cant retrieve'
                # если не обрабатывать - просто получается пустое поле, его можно обработать дальше
                pass

        # В это месте у нас есть объекты фильма 'm' и актера 'pers'
        d = Duty(person=pers, movi=m, department='', character=actor.character, job='', order=actor.order)
        d.save()
