#CSV Files from: http://ssd.jpl.nasa.gov/?horizons
#TLE Files from: http://space-track.org/
'''
version 0.3
created: olsen
edited: 2012-12-20 olsen
notes:
- new order 
- fixed some datasource
edited: 2012-12-14 flx
notes: 
- added RZALT SETTINGS (RZALT for json exports to be interpreted by html interface)
- added 'category' to CELESTIAL_BODY
- added 'active' flag to CELESTIAL_BODY
- added 'color' for html representation (hex, rgb, rgba) 
- removed multiline commnts in array
- added observer var
- added CELESTIAL_BODY_CATEGORIES dict for html order
- functional change: 
  removed 'import ephem' and 
  replaced 'class':ephem.Sun() to 'class':'ephem.Sun()' (as string)
  to be loaded by eval(obj['class'])
edited: 2012-12-15 flx
notes: 
- added 'pic' to CELESTIAL_BODY
- added 'symbol' to CELESTIAL_BODY
- added 'name' to CELESTIAL_BODY

'''

EXCHANGE_JSON_FILE = "data.json"

RZALT_JSON_OUTPUT = "stdout" # or: file
RZALT_JSON_FILE = "rzalt.json"
RZALT_TIMESPAN_HOURS = 7

OBSERVER = 'ephem.city("Zurich")'

CELESTIAL_BODY_CATEGORIES = {
    "planets":{
        'name':'a. Planeten unseres Sonnensystems',
        'sort':0,
        },
    "earthsatellites":{
        'name':'b. Erdtrabanten',
        'sort':1,
        },
    "spacedebris":{
        'name':'c. Weltraumschrott',
        'sort':2,
        },
    "spaceprobes":{
        'name':'d. Raumsonden',
        'sort':3,
        },
    "stars":{
        'name':'e. Sterne',
        'sort':4,
        },
    "comets":{
        'name':'f. Kometen',
        'sort':5,
        },
    "asteroids":{
        'name':'g. Asteroiden',
        'sort':6,
        },
    "constellations":{
        'name':'h. Konstellationen',
        'sort':7,
        },
}
CELESTIAL_BODY = {
	
    "sun": {
        'active': 1,
        'name': 'Sonne',
        'category': 'stars',
        'color': '#ffff00',
        'symbol':'Sun_symbol.svg',
        'datatype': 'pyephem', # Sun
        'class': 'ephem.Sun()'
        },
        
# Planeten___Planets____________________________________________________

    "mercury": {
        'active': 1, 
        'name': 'Merkur',
        'category': 'planets',
        'color': 'blue',
        'symbol':'Mercury_symbol.svg',
        'datatype': 'pyephem',
        'class': 'ephem.Mercury()'
    },
    "venus": { 
        'active': 1,
        'name': 'Venus',
        'category': 'planets',
        'color': 'green',
        'symbol':'Venus_symbol.svg',
        'datatype': 'pyephem', #Venus/Hesperus/Stella Maris/Abendstern/Morgenstern
        'class': 'ephem.Venus()'
    },
    "mars": {
        'active': 1,
        'name': 'Mars',
        'category': 'planets',
        'color': 'red',
        'symbol':'Mars_symbol.svg',
        'datatype': 'pyephem',
        'class': 'ephem.Mars()'
    },
    "jupiter": {
        'active': 1,
        'name': 'Jupiter',
        'category': 'planets',
        'color': 'lightblue',
        'symbol':'Jupiter_symbol.svg',
        'pic':'pic-jupiter.png',
        'datatype': 'pyephem',
        'class': 'ephem.Jupiter()'
    },
    "saturn": {
        'active': 1,
        'name': 'Saturn',
        'category': 'planets',
        'color': 'pink',
        'pic':'pic-saturn.png',
        'symbol':'Saturn_symbol.svg',
        'datatype': 'pyephem',
        'class': 'ephem.Saturn()'
    },
    "uranus": {
        'active': 1,
        'name': 'Uranus',
        'category': 'planets',
        'color': 'brown',
        'symbol':'Uranus_symbol.svg',
        'datatype': 'pyephem',
        'class': 'ephem.Uranus()'
    },
    "neptune": {
        'active': 1,
        'name': 'Neptun',
        'category': 'planets',
        'color': 'violett',
        'symbol':'Neptune_symbol.svg',
        'datatype': 'pyephem',
        'class': 'ephem.Neptune()'
    },
    
#Erdtrabanten__Earth-satellites_________________________________________
    "moon": {
        'active': 1,
        'name': 'Mond',
        'category': 'earthsatellites',
        'color': 'orange',
        'symbol':'Moon_symbol.svg',
        'pic':'pic-moon.png',
        'datatype': 'pyephem',
        'class': 'ephem.Moon()'
    },    
    "iss": {
        'active': 1,
        'name': 'ISS (Internationale Raumstation)',
        'category': 'earthsatellites',
        'color': '#ffffff',
        'symbol':'ISS_insignia.svg',
        'datatype': 'tle',
        'sourcefile': 'data/tle/catalog.txt', 
        # or http://www.celestrak.com/NORAD/elements/amateur.txt
    },
    
#Raumsonden__Space-Probes_______________________________________________
    "voyager1": {
        'active': 1,
        'name': 'Voyager 1',
        'category': 'spaceprobes',
        'color': '#ffffff',
        'symbol':'Voyager_symbol.svg',
        'datatype': 'nasacsv',
        'sourcefile': 'data/nasacsv/voyager_1.csv',
    },
    "voyager2": {
        'active': 1,
        'name': 'Voyager 2',
        'category': 'spaceprobes',
        'color': '#ffffff',
        'symbol':'Voyager_symbol.svg',
        'datatype': 'nasacsv',
        'sourcefile': 'data/nasacsv/voyager_2.csv',
    },
    "hubble": {
        'active': 0,
        'name': 'HST',
        'category': 'spaceprobes',
        'color': '#ffffff',
        'symbol':'Hubble_logo.svg',
        'datatype': 'tle',
        'sourcefile': 'data/tle/catalog.txt', 
    },
    
#Weltraumschrott__Space_Debris__________________________________________
	"envisat": {
        'active': 1,
        'name': 'Envisat',
        'category': 'spacedebris',
        'color': '#ffffff',
        'datatype': 'tle', 
        'sourcefile': 'data/tle/catalog.txt', # or http://www.celestrak.com/Norad/elements/visual.txt
    },
    #Vanguard 1
    "vanguard_1": {
        'active': 0,
        'name': 'Vanguard 1',
        'category': 'spacedebris',
        'color': '#ffffff',
        'datatype': 'tle',
        'sourcefile': 'data/tle/catalog.txt',
    },
    #Cosmos 382 
    "cosmos_382": {
        'active': 0,
        'name': 'Cosmos 382',
        'category': 'spacedebris',
        'color': '#ffffff',
        'datatype': 'tle',
        'sourcefile': 'data/tle/catalog.txt',
    },
    #Kosmos 1818 
    "cosmos_1818": {
        'active': 0,
        'name': 'Cosmos 1818',
        'category': 'spacedebris',
        'color': '#ffffff',
        'datatype': 'tle',
        'sourcefile': 'data/tle/catalog.txt',
    },
    
#Sterne___Stars_________________________________________________________
    "aldebaran": {
        'active': 1,
        'name': 'Aldebaran (α Tauri)',
        'category': 'stars',
        'color': '#ffffff',
        'symbol':'Alpha_symbol.svg',
        'distance': '65ly',
        'datatype': 'pyephem',
        'class': 'ephem.star("Aldebaran")'
    },
    "antares": {
        'active': 1,
        'name': 'Antares (α Scorpii)',
        'category': 'stars',
        'color': '#ffffff',
        'pic':'pic-antares.png',
        'distance': '550ly',
        'datatype': 'pyephem',
        'class': 'ephem.star("Antares")'
    },
    "sirius": {
        'active': 1,
        'name': 'Sirius (α Canis Majoris)',
        'category': 'stars',
        'color': '#ffffff',
        'pic':'pic-antares.png',
        'distance': '550ly',
        'datatype': 'pyephem',
        'class': 'ephem.star("Sirius")'
    },
    "polaris": {
        'active': 1,
        'name': 'Polaris (α Ursae Minoris)',
        'category': 'stars',
        'color': '#ffffff',
        'pic':'pic-antares.png',
        'distance': '550ly',
        'datatype': 'pyephem',
        'class': 'ephem.star("Polaris")'
    },
    "vega": {
        'active': 1,
        'name': 'Vega',
        'category': 'stars',
        'color': '#ffffff',
        'pic':'pic-antares.png',
        'distance': '550ly',
        'datatype': 'pyephem',
        'class': 'ephem.star("Vega")'
    },
    
    
#Sternkonstellationen___Constellations__________________________________
	#Cassopeia -> using star Schedar which is part of the constellation
	"cassopeia": {
        'active': 1,
        'name': 'Cassopeia',
        'category': 'constellations',
        'color': '#ffffff',
        'symbol':'Cassiopeia.svg',
        'pic':'pic-cassiopeia.png',
        'distance': '228ly',
        'datatype': 'pyephem', 
        'class': 'ephem.star("Schedar")'
    },
	#Southerncross -> using star Mimosa which is part of constellation
	"southerncross": {
        'active': 1,
        'name': 'S&uuml;dkreuz (Crux)',
        'category': 'constellations',
        'color': '#ffffff',
        'symbol':'Southerncross.svg',
        'pic':'pic-southerncross.png',
        'distance': '280ly',
        'datatype': 'pyephem', 
        'class': 'ephem.star("Mimosa")'
    },
	#Big Bear or Das Reiterlein im grossen Wagen -> using star Megrez 
	"big_bear": {
        'active': 1,
        'name': 'Grosser B&auml;r (Ursa Major)',
        'category': 'constellations',
        'color': '#ffffff',
        'symbol':'Big_Bear-Ursa_Major.svg',
        'pic':'pic-big_bear-ursa_major.png',
        'distance': '58.4ly',
        'datatype': 'pyephem', 
        'class': 'ephem.star("Megrez")'
    },
    #Orion -> using Betelgeuse
    "orion": {
        'active': 1,
        'name': 'Orion',
        'category': 'constellations',
        'color': '#ffffff',
        'symbol':'Orion_IAU.svg',
        'pic':'pic-orion.png',
        'distance': '8.60ly',
        'datatype': 'pyephem', 
        'class': 'ephem.star("Betelgeuse")'
    },

#Asteroiden___Asteroids_________________________________________________
    "243_Ida": {
        'active': 1,
        'name': '243 Ida',
        'category': 'asteroids',
        'color': '#ffffff',
        'datatype': 'nasacsv',
        'sourcefile': 'data/nasacsv/243_Ida.csv',
    },
    "2010_TK7": {
        'active': 1,
        'name': '2010 TK7',
        'category': 'asteroids',
        'color': '#ffffff',
        'datatype':  'nasacsv',
        'sourcefile': 'data/nasacsv/2010_TK7.csv',
    },
#Kometen___comets_______________________________________________________
	#Georges Perec
		#unknown
	#1P/Halley
    "halley": {
        'active': 1,
        'name': 'Halley',
        'category': 'comets',
        'color': '#ffffff',
        'datatype': 'nasacsv',
        'sourcefile': 'data/nasacsv/halley.csv',
    },
	#ISON C/2012 S1 
    "ISON": {
        'active': 1,
        'name': 'ISON',
        'category': 'comets',
        'color': '#ffffff',
        'datatype': 'nasacsv',
        'sourcefile': 'data/nasacsv/ISON.csv', 
	},
#Galaxien___Galaxies____________________________________________________
    #M 31 aka Andromeda Galaxy aka C/2002 Y1 (Juels-Holvorcem)
    #Data from http://www.maa.mhn.de/Tools/Xephem/Messier.edb
    "M31": {
        'active': 0,
        'name': 'M 31',
        'category': 'galaxies',
        'color': '#ffffff',
        'datatype': 'pyephem',
        'class': 'ephem.readdb("M31,f|G,0:42:44,+41:16:8,4.16,2000,11433|3700|35")', 
    },
#Gegenerde___Globus_Cassus______________________________________________
	#Antichton
	"antichton": {
        'active': 1,
        'name': 'Antichton - Gegenerde',
        'category': 'stars',
        'color': '#ffff00',
        'datatype': 'pyephem', # Same direction as the Sun
        'class': 'ephem.Sun()'
        },
}

