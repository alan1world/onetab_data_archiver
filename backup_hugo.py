#!/usr/bin/python3
# -*- coding: utf-8 -*-

def create_hugo(content, browser='chrome', hdate='', location = "/home/human1/Web/hugo/content/post/daily.md", modifier = ''):

    hline = '''+++\n'''
    header_text = ""
    header_text = hline + '''date = "''' + hdate + '''"\n'''
    header_text = header_text + '''title = "''' + browser + ' ' + hdate + '''"\n\n''' + hline + '\n'
    full_text = header_text + content
    with open(location, 'w') as file:
        file.write(full_text)
        
def create_namedtuple(content, browser='chrome', hdate='', location = "/home/human1/Web/hugo/content/post/daily.md", modifier = ''):

    hline = '''+++\n'''
    header_text = ""
    header_text = hline + '''date = "''' + hdate + '''"\n'''
    header_text = header_text + '''title = "''' + browser + ' ' + hdate + '''"\n\n''' + hline + '\n'
    full_text = header_text
    for x in content:
        full_text += x.raw_link + '\n\n'
    with open(location, 'w') as file:
        file.write(full_text)
