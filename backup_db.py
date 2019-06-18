#!/usr/bin/python3
# -*- coding: utf-8 -*-

import dataset

def create_db(content, source, output_name='daily.db'):
    
    db = dataset.connect('sqlite:///'+output_name)
    table = db['links']
    for x in content:
        table.insert(dict(raw_link=x.raw_link, title=x.title, link=x.link, source=source))
