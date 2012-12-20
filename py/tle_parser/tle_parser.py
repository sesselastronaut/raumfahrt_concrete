import math
import ephem
import fileinput, sys, string


def get_tle_az(tle_file, satelite_name, city):
	import ephem
	data_headline, data_row_1, data_row_2 = get_tle_data(tle_file, satelite_name)
	satellite = ephem.readtle(data_headline,data_row_1,data_row_2)
	satellite.compute(city)
	return satellite.az

def get_tle_data(tle_file, satelite_name):
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
		#print "Satelite:" + satelite_name
		splitted_line = line.split(' ')
		if satelite_name.upper() in line: #splitted_line[0] == satelite_name.upper():
			headline_num = line_number
			data_headline = line
			#print "Sateliteupper:" + satelite_name.upper()
			#print data_headline
			
		if headline_num != 0 and line_number == headline_num+1:
			data_row_1 = line
			#print data_row_1
		if headline_num != 0 and line_number == headline_num+2:
			data_row_2 = line
	return data_headline,data_row_1,data_row_2
