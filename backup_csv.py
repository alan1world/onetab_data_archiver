#!/usr/bin/python3
# -*- coding: utf-8 -*-

import html, csv

def create_csv(link_text, output_name='daily.csv'):

    with open(output_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["raw_link", "title", "link"])
        for x in link_text:            
            csv_writer.writerow([html.escape(x.raw_link, quote=True),html.escape(x.title, True), x.link])
