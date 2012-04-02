#!/usr/bin/env python
#coding: utf-8

#git clone https://github.com/dbr/themoviedb.git

import tmdb
from tmdb import *
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s \t %(message)s',datefmt='%d/%m/%Y %H:%M',filename='/home/swasher/kinobox/log',level=logging.DEBUG)

class movi:
    pass

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

#get_list_by_name('China')


    #mov.released=movie['released']
    #print movie['overview']
    #full = first.info()
    #print unicode(full['plot']