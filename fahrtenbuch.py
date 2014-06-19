#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Create a rock climbing "fahrtenbuch" using the klefue.kf3
    from http://db-sandsteinklettern.gipfelbuch.de

    TODO:
    - export data to LaTeX
      - link to osm with GPS coordinates
"""

import os
# apt-get install python-sqlite
from pysqlite2 import dbapi2 as sqlite


import klefue


klefuefile = "klefue.klf"

if os.path.exists("./"+klefuefile):
    print "Found "+klefuefile+", loading database..."
    Klefue = klefue.Klefue(klefuefile)
else:
    print "Could not find "+klefuefile
    exit(1)


a = raw_input("Search for a peak. ['hunskirche'] ").decode("utf-8")
if len(a) == 0:
    a = 'hunskirche'

ret = Klefue.search_peak(a)
# List the peaks available

# print results
i = 1
for item in ret:
    pstring = u"[{}] ".format(i)
    i += 1
    for sub in item:
        pstring += sub + "  "
    print pstring

b = raw_input("Display routes from which peak? ['1']").decode("utf-8")
if len(b) == 0:
    b = 1

peakid = Klefue.get_peak_id(ret[int(b)-1])

for route in Klefue.get_peak_routes(peakid):
    s = u""
    for item in route:
        s += item.strip() + "  "
    print s


import IPython
IPython.embed()

# http://www.devshed.com/c/a/Python/Using-SQLite-in-Python/1/
#connection = sqlite.connect('test.db')
#cursor = connection.cursor()

