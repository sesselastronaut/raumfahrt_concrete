# -*- coding: utf-8 -*-
from config import *
try:
    import json
except:
    import simplejson as json
import time
import sys
from pprint import pprint
from nasa_csvparser import nasa_csvparser
from tle_parser import tle_parser
import logging
import ephem
import math
from serial_com import SerialCom

degrees_per_radian = 180.0 / math.pi

def celestial_body_func():
	# Log everything, and send it to stderr.
	FORMAT = "%(asctime)-15s %(message)s"
	logging.basicConfig(format=FORMAT,level=logging.DEBUG,datefmt='%Y-%m-%d %H:%M:%S')

	#Object creation
	
	sc = SerialCom()
	#sc.resetBedFromLog()
	

	while 1:
		logging.debug("-----------------------------")
		logging.debug("READING JSON FILE")
		data = json.load(open(EXCHANGE_JSON_FILE))
		'''
		with open(EXCHANGE_JSON_FILE) as data_file:
		data = json.load(data_file)
		'''
		goto = data["goto"]
		logging.debug("goto: " + goto)
	# where are we heading to?
		if not CELESTIAL_BODY[goto]:
			logging.debug("OUT OF ORBIT - could not match celestial body from json file")
			continue
		celestial_body = CELESTIAL_BODY[goto]

		if celestial_body["datatype"] == 'pyephem':
			logging.debug("using pyephem")
			city = eval(OBSERVER)
			position = eval(celestial_body["class"])
			position.compute(city)
			position = position.az * degrees_per_radian

		elif celestial_body["datatype"] == 'nasacsv':
			logging.debug("using nasa_csvparser")
			csvfile =  celestial_body["sourcefile"]
			position = nasa_csvparser.get_position(csvfile)
			logging.debug("London GMT / UTC time:" + position["date"])
			position = position["azi"]
		
		elif celestial_body["datatype"] == 'tle':
			logging.debug("using tle parser")
			tle_file =  open (celestial_body["sourcefile"])
			city = eval(OBSERVER)
			satelite_name = celestial_body["parsekey"] #goto
			position = tle_parser.get_tle_az(tle_file, satelite_name, city) * degrees_per_radian
		else:
			logging.debug("ERRRRRRRRRRRROR. Config file is wrong")
			continue
	# send to serial port

		#print("PositionText:"+str(int(float(position)*10)))
		positionTruncInt = int(10*float(position))
		positionTruncFloat = float(positionTruncInt)/10
		print(positionTruncFloat)
		
		
		sc.setBedPosition(positionTruncFloat)
		logging.debug("Sending to serial:")
		logging.debug(position)

		time.sleep(1)
		sc.receiveData()
		sc.logBedData()
		
		
		#sc.receiveData()
