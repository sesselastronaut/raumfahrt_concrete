# -*- coding: utf-8 -*-
from nasa_csvparser.nasa_csvparser import *

file = "data/nasa_csvparser/voyager_1.csv"
voyager_position = get_position(file)
print voyager_position
print "Date: " + voyager_position["date"]
print "AZI: " + voyager_position["azi"]
print "ELEV: " + voyager_position["elev"]
