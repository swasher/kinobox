#!/usr/bin/env python
#coding: utf-8

#git clone https://github.com/dbr/themoviedb.git

import tmdb
from tmdb import *
import logging

from tmdb3 import set_key
from tmdb3 import get_locale, set_locale
from tmdb3 import searchMovie
from tmdb3 import set_cache


logging.basicConfig(format='%(asctime)s %(levelname)s \t %(message)s',datefmt='%d/%m/%Y %H:%M',filename='/home/swasher/kinobox/log',level=logging.DEBUG)

class movi:
    pass

def get_list_by_name(zapros):
    set_key('c97c17e619252e35bad2e158d4211fcc')
    set_locale('ru', 'ru')
    set_cache(engine='file', filename='~/.tmdb3cache')

    results = searchMovie(zapros)
    #results = searchMovie(unicode('Ameli'))
    answer=[]
    i=0
    aa=len(results)
    for movie in results[0:10]:
        mov=movi()
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

"""
def get_list_by_name(zapros):
    results = tmdb.search(unicode(zapros))
    #return results
    answer=[]
    i=0
    for movie in results:
        mov=movi()
        #print unicode(results[i])
        searchResult = results[i]
        mov.id=searchResult['id']
        mov.title=searchResult['name']
        mov.year=str(searchResult['released'])[0:4]
        mov.overview=searchResult['overview']
        mov.url=searchResult['url']
        mov.altname=searchResult['alternative_name']
        mov.origname=searchResult['original_name']
        try:
            mov.poster=searchResult['images'][0]['w154']
        except:
            mov.poster=''
        answer.append(mov)
        i+=1
    return answer
"""

#get_list_by_name('China')


    #mov.released=movie['released']
    #print movie['overview']
    #full = first.info()
    #print unicode(full['plot']