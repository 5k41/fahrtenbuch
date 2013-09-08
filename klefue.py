#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    access the rock climbing data base at
    http://db-sandsteinklettern.gipfelbuch.de

    Download of the database from
    http://db-sandsteinklettern.gipfelbuch.de/download
    http://db-sandsteinklettern.gipfelbuch.de/daten/klefue.klf

    TODO:
    deal with gipfelname_de/gipfelname_cz
"""


class Klefue(object):
    def __init__(self, klefuefile, encoding="windows-1252" ):
        f = open(klefuefile, 'r')
        data = f.readlines()
        index = list()
        for i in range(len(data)):
            line = data[i]
            data[i] = line.decode(encoding)
            if line[0] == "$":
                index.append([i, line.strip().strip("$:").lower(),
                             data[i+1].lower().strip().split("\t")])
        self.index = index
        self.rawdata = data

    def get_header(self, tablename):
        """ Returns the header data of the klefue tables.
            Argument must be something like "gipfel" or "gebiet".
            This information is taken from self.index.
        """
        for item in self.index:
            if tablename.lower().strip() == item[1].lower():
                return item[2]

    def get_columns(self, data, columnnames, tablename):
        """ From a list of data from a table with tablename (e.g. "gipfel"),
            get only columns listed in columnnames.
            Possible columnnames can be found using the get_header function.
        """
        results = list()
        availcolumns = self.get_header(tablename)
        for line in data:
            newline = list()
            for column in columnnames:
                colid = availcolumns.index(column.lower())
                newline.append(line[colid])
            results.append(newline)
        return results

    def search(self, word, typeres=None):
        """ search for a particular word in klefue file and return information
            typeres can be "gipfel" (any item in self.index). In this case, not
            the entire dictionary is returned but only a list corresponding
            to typeres.
        """
        word = word.strip()
        # dictionary with line numbers as keys
        searchdata = dict()
        for i in range(len(self.rawdata)):
            line = self.rawdata[i]
            if line.lower().count(word.lower()) > 0:
                searchdata[i] = line.strip()

        # dictionary with self.index data as keys
        results = dict()
        for item in self.index:
            results[item[1]] = list()
        for key in searchdata.keys():
            for j in range(len(self.index)):
                if key > self.index[j][0] and key < self.index[j+1][0]:
                    results[self.index[j][1]].append(searchdata[key].split("\t"))
        if typeres is not None:
            typeres = typeres.strip()
            return results[typeres.lower()]
        else:
            return results

    def search_peak(self, word):
        """ Find all peaks that have word in their name.
        """
        return self.search(word, typeres="gipfel")

    def get_peak_routes(self, peakid):
        """ Using the identifier of a peak, get the list of routes.
        """
        results = list()
        for i in range(len(self.rawdata)):
            line = self.rawdata[i]
            try:
                if line.split("\t")[0] == peakid:
                    results.append(line.split("\t"))
            except:
                pass
        return results

    def get_peak_id(self, proplist):
        """ Using the list that we create, when we call search_peak,
            return the peak id.
        """
        # Check with get_header("gipfel")
        return proplist[1]

if __name__ == "__main__":
    klefuefile = "klefue.kf3"
    klefue = Klefue(klefuefile)
    a=klefue.search("hunskirche", "gipfel")
    columns = ["gipfelname_d", "gipfelid", "gipfelnord", "gipfelost"]


    b=klefue.get_columns(a, columns, "gipfel")

    print b
