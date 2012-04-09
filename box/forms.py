#!/usr/bin/env python
#coding: utf-8
__author__ = 'swasher'

from django import forms
from models import Movi

YEAR_CHOISE=Movi.objects.values_list('id', 'year').order_by('year').distinct('year')
    #(a.id, a.year) for a in Movi.objects.all()
    #y = Movi.objects.values_list('id', 'year').order_by('year').distinct('year')

    # tuple must be:
    #[(1999, 1999), (2000, 2000)]


class SelectForm(forms.Form):
    movie = forms.ChoiceField(choices=YEAR_CHOISE)
