#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    access the rock climbing data base at
    http://db-sandsteinklettern.gipfelbuch.de

    Download of the database from
    http://db-sandsteinklettern.gipfelbuch.de/download
    (update ("aktualisieren") the database for .klf
     "Datei klefue.klf aktualisieren [click]"      )
    http://db-sandsteinklettern.gipfelbuch.de/daten/klefue.klf

    TODO:
    deal with gipfelname_de/gipfelname_cz
"""
from __future__ import print_function

class Klefue(object):
    def __init__(self, klefuefile, encoding="windows-1252" ):
        f = open(klefuefile, 'r', encoding=encoding)
        data = f.readlines()
        index = list()
        for i in range(len(data)):
            #line = data[i]
            #data[i] = line.decode(encoding)
            if data[i][0] == "$":
                index.append([i, data[i].strip().strip("$:").lower(),
                             data[i+1].lower().strip().split("\t")])
        self.index = index
        self.rawdata = data
        
        # Create dictionaries for regions and sectors, and peaks
        # Gebiet
        self.regions = dict()
        for i in range(self.index[0][0]+2,self.index[1][0]-1):
            line = self.rawdata[i]
            a = line.split("\t")
            a[0] = int(a[0])
            self.regions[a[0]] = a

        # Teilgebiet
        self.sectors = dict()
        for i in range(self.index[1][0]+2,self.index[2][0]-1):
            line = self.rawdata[i]
            a = line.split("\t")
            a[0] = int(a[0])
            a[1] = int(a[1])
            self.sectors[a[1]] = a

        # Gipfel
        self.peaks = dict()
        for i in range(self.index[2][0]+2,self.index[3][0]-1):
            line = self.rawdata[i]
            a = line.split("\t")
            a[0] = int(a[0])
            a[1] = int(a[1])
            self.peaks[a[1]] = a

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
            for j in range(len(self.index)-1):
                if key > self.index[j][0] and key < self.index[j+1][0]:
                    results[self.index[j][1]].append(searchdata[key].split("\t"))
            if key > self.index[j][0]:
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
        
        
    def get_peak_region_and_sector_names(self, peakid):
        """ Using the identifier of a peak, get the region
            and area of that peak.
        """
        secid = self.get_sector_id_from_peak_id(peakid)
        sector = self.sectors[secid]
        regid = self.get_region_id_from_peak_id(peakid)
        region = self.regions[regid]
        return [region[1], sector[2]]


    def get_region_id_from_peak_id(self, peakid):
        # get sector
        secid = self.peaks[peakid][0]
        sector = self.sectors[secid]
        # get region
        return sector[0]
        
        
    def get_sector_id_from_peak_id(self, peakid):
        # get sector
        secid = self.peaks[peakid][0]
        # get region
        return secid
        

    def get_peak_id(self, proplist):
        """ Using the list that we create, when we call search_peak,
            return the peak id.
        """
        # Check with get_header("gipfel")
        return proplist[2]

if __name__ == "__main__":
    klefuefile = "klefue.klf"
    KF = Klefue(klefuefile)
    route_columns = ["WEGNAME_D", "SCHWIERIGKEIT", "WEGNR",
                     "WEGBESCHREIBUNG_D"]
    peak_columns = ["gipfelname_d", "gipfelid", "gipfelnord",
                    "gipfelost"]
    while True:
        print("What do you want to search for? \n"+
              "1. Peak (Gipfel) \n"+
              "2. Route (Weg) \n")
        choice = input()
        # Check for valid choice
        if choice == "1":
            stype = "gipfel"
            columns = peak_columns
            break
        elif choice == "2":
            stype = "wege"
            columns = route_columns
            break
    print("Type a name.\n")
    search = input()
    
    a=KF.search(search, stype)
    a.sort()

    if stype == "gipfel":
        print("For which peak do you want to display the routes?")
        printdata = list()
        for i in range(len(a)):
            nam = KF.get_peak_region_and_sector_names(int(a[i][1]))
            printdata.append(nam)
        printdata.sort()
        
        for i in range(len(a)):
            nam = printdata[i]
            print("{}. {} - {} - {}".
                  format(i, nam[0], nam[1], a[i][2]))
        q = int(input())
        if q in range(len(a)):
            a = KF.get_peak_routes(a[q][1])
        columns = route_columns
        stype = "wege"
        
    b=KF.get_columns(a, columns, stype)
    b.sort()
    for i in range(len(b)):
        print("{} \t {} \t {} \t {}".
              format(b[i][0], b[i][1], b[i][2], b[i][3]))

    import IPython
    IPython.embed()
