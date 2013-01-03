import math
import ephem
import fileinput, sys, string


def get_tle_az(tle_file, satelite_parsekey, city):
	import ephem
	data_headline, data_row_1, data_row_2 = get_tle_data(tle_file, satelite_parsekey)
	satellite = ephem.readtle(data_headline,data_row_1,data_row_2)
	satellite.compute(city)
	return satellite.az

def get_tle_data(tle_file, satelite_parsekey):
	tles = []
	tle = []
	line_number = 0
	headline_num = 0
	data_headline = ''
	data_row_1 = ''
	data_row_2 = ''

	#print tle_file
	#lines = tle_file.readlines()
	for line in tle_file.readlines():
		line_number += 1
		#print line_number
		#print "Satelite:" + satelite_parsekey
		splitted_line = line.split(' ')
		if satelite_parsekey.upper() in line: #splitted_line[0] == satelite_parsekey:
			headline_num = line_number
			data_headline = line
			#print "Sateliteupper:" + satelite_parsekey
			#print data_headline
			
		if headline_num != 0 and line_number == headline_num+1:
			data_row_1 = line
			#print "1.TLE ROW"
			#print data_row_1
		if headline_num != 0 and line_number == headline_num+2:
			data_row_2 = line
			#print "2.TLE ROW"
			#print data_row_2
	return data_headline,data_row_1,data_row_2
