#!/usr/bin/env python
# encoding: utf-8
"""
bixi.py
parse Montreal bixi station data and output kml for consumption by map services
Created by olivier Thereaux on 2009-05-16.
Updated 2011-09 to add Toronto 
Uses public, but undocumented and unofficial, data source.
USE AT YOUR OWN RISKS
"""

import sys
import os
import xml.etree.cElementTree as ET
from urllib2 import urlopen
import re

def main():
    print """<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://earth.google.com/kml/2.1">
    <Document><name>Bixi</name><Style id="BixiIconStyle"><scale>1,.5</scale><IconStyle><Icon><href>http://olivier.thereaux.net/2009/05/bixi_icon.png</href></Icon></IconStyle></Style>
    """
    for URL in ["https://toronto.bixi.com/data/bikeStations.xml", "https://montreal.bixi.com/data/bikeStations.xml"]:
        feed = urlopen(URL)
        tree = ET.parse(feed)
        for station in tree.getroot().findall("station"):
            nbBikes = station.find("nbBikes").text
            nbEmptyDocks = station.find("nbEmptyDocks").text
            station_lat = re.sub(r"\s", "", station.find("lat").text)
            station_long = re.sub(r"\s", "", station.find("long").text.strip())
            station_installed = station.find("installed").text
            station_locked = station.find("locked").text
            if (station_installed == "true" and station_locked != "true" and (nbBikes != "0" or nbEmptyDocks != "0")):
                print "<Placemark><name>%s bikes avail. - %s empty slots</name><styleUrl>#BixiIconStyle</styleUrl><Point><coordinates>%s,%s,0</coordinates></Point></Placemark>" % (nbBikes, nbEmptyDocks, station_long, station_lat)
        feed.close()
    print "</Document></kml>"
    
if __name__ == '__main__':
  main()

