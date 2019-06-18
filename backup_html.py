#!/usr/bin/python3
# -*- coding: utf-8 -*

import mistune

def create_html(content, browser='chrome', hdate='', location = '/home/human1/Web/www/main/', modifier = ''):

    build_content = ""
    for x in content:
        build_content += x.raw_link + "\n\n"
    
    myfinaltext = '''<!doctype html>\n<html lang="en">\n<head>\n    <meta charset="utf-8">\n    <title>'''
    myfinaltext = myfinaltext + "Links for " + browser + ' ' + hdate
    myfinaltext = myfinaltext + '''</title>\n</head>\n<body>''' + mistune.markdown(build_content) + '''</body>\n</html>'''
    with open(location, 'w') as file:
        file.write(myfinaltext)
