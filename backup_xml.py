#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.etree.ElementTree import Element, ElementTree

def create_xml(link_text, output_name='daily.xml'):

    top = Element('root')
    children = [Element('doc', raw_link=linker.raw_link, title=linker.title, link=linker.link) for linker in link_text]
    top.extend(children)
    tree = ElementTree(top)
    tree.write(open(output_name, 'wb'))
