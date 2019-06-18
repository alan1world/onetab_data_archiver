#!/usr/bin/python3
# -*- coding: utf-8 -*-

from collections import namedtuple

def clean(thetext):
    
    if thetext.startswith('chrome-extension'):
        location = thetext.find("uri=http")
        return thetext[location+4:].strip()
    else:
        return thetext.strip()

def create_namedtuple(mytext, mydate,mybrowser='chrome'):

    Linker = namedtuple('Linker', ['raw_link', 'browser', 'date', 'title', 'link'])
    
    link_collection = []
    for link_item in mytext:
        if link_item == '':
            continue
        elif mybrowser in ['chrome', 'firefox']:
            try:
                b,a = link_item.split(r"|",1)
            except:
                continue
        elif mybrowser == 'keep':
            try:
                a,b = link_item.rsplit(r"|",1)
            except:
                continue
        else:
            raise ValueError('Currently accepted browser options are: chrome, firefox, keep')
        c = clean(a)
        d = clean(b)
        link_collection.append(Linker("["+c+"]"+"("+d+")",mybrowser,mydate,c,d))
    return link_collection
