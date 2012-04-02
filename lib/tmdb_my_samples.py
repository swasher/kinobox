#!/usr/bin/env python
#coding: utf-8

import tmdb
from tmdb import *
results = tmdb.search("Fight Club")

#first - первое кино из всех найденых результатов
movie = results[0]
movie = MovieDb.

#print movie.keys()
# ['rating', 'votes', 'name', 'language', 'certification', 'url', 'overview', 'images', 
# 'popularity', 'original_name', 'last_modified_at', 'imdb_id', 'released', 'score', 
# 'adult', 'version', 'translated', 'type', 'id', 'alternative_name']




images=movie['images']
#print images
### [<Image (poster for ID 4ea5cc8334f8633bdc000a59)>, <Image (backdrop for ID 4ec23b495e73d6476b004f09)>]
#print type(images)
### <class 'tmdb.ImagesList'>
### - то есть movie.image - это список из двух объектов, - постера и "заднего фона", которые являются словарями



poster=images[0]
#print poster
###<Image (poster for ID 4ea5cc8334f8633bdc000a59)>
#print type(poster)
###<class 'tmdb.Image'>
#print poster.keys()
###['w154', 'cover', 'mid', 'original', 'w342', 'type', 'id']

for key in poster.keys():
   print key, 'is ', poster[key]
   ## w154     is  http://cf2.imgobject.com/t/p/w154/2lECpi35Hnbpa4y46JX0aY3AWTy.jpg
   ## cover    is  http://cf2.imgobject.com/t/p/w185/2lECpi35Hnbpa4y46JX0aY3AWTy.jpg
   ## mid      is  http://cf2.imgobject.com/t/p/w500/2lECpi35Hnbpa4y46JX0aY3AWTy.jpg
   ## original is  http://cf2.imgobject.com/t/p/original/2lECpi35Hnbpa4y46JX0aY3AWTy.jpg
   ## w342     is  http://cf2.imgobject.com/t/p/w342/2lECpi35Hnbpa4y46JX0aY3AWTy.jpg
   ## type     is  poster
   ## id       is  4ea5cc8334f8633bdc000a59


#Чтобы узнать жанры, прийдется вытащить всю инфу

info=movie.info()
for genreName in info['categories']['genre']:
   print "%s (%s)" % (genreName, info['categories']['genre'][genreName])
   #print "{0} ({1})".format(genreName, info['categories']['genre'][genreName])

