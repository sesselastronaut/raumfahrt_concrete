# -*- coding: utf-8 -*-
from nasa_csvparser.nasa_csvparser import *

file = "nasa_csvparser/VoyagerI.txt"
voyager_position = get_position(file)
print voyager_position
print "Date: " + voyager_position["date"]
print "AZI: " + voyager_position["azi"]
print "ELEV: " + voyager_position["elev"]
