#CSV Files from: http://ssd.jpl.nasa.gov/?horizons
#TLE Files from: http://space-track.org/
'''
version 0.4
created: olsen
edited: 2013-1-4 olsen
notes: 
- added parsekey to config for tlefiles
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
    "globus_cassus":{
        'name':'e. Gegenerde',
        'sort':4,
        },
    "stars":{
        'name':'f. Sterne',
        'sort':5,
        },
    "comets":{
        'name':'g. Kometen',
        'sort':6,
        },
    "asteroids":{
        'name':'h. Asteroiden',
        'sort':7,
        },
    "constellations":{
        'name':'i. Konstellationen',
        'sort':8,
        },
    "galaxies":{
        'name':'j. Galaxien',
        'sort':9,
        },
}
CELESTIAL_BODY = {
	
    "sun": {
        'active': 1,
        'name': 'Sonne',
        'category': 'stars',
        'color': '#ffff00',
        'symbol':'Sun_symbol.svg',
        'pic':'pic-sun.png',
        'datatype': 'pyephem',
        'class': 'ephem.Sun()',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
        },
        
# Planeten___Planets____________________________________________________

    "mercury": {
        'active': 1, 
        'name': 'Merkur',
        'category': 'planets',
        'color': 'blue',
        'symbol':'Mercury_symbol.svg',
        'pic':'pic-mercury.png',	
        'datatype': 'pyephem',
        'class': 'ephem.Mercury()',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "venus": { 
        'active': 1,
        'name': 'Venus',
        'category': 'planets',
        'color': 'green',
        'symbol':'Venus_symbol.svg',
        'pic':'pic-venus.png',
        'datatype': 'pyephem', #Venus/Hesperus/Stella Maris/Abendstern/Morgenstern
        'class': 'ephem.Venus()',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "mars": {
        'active': 1,
        'name': 'Mars',
        'category': 'planets',
        'color': 'red',
        'symbol':'Mars_symbol.svg',
        'pic':'pic-mars.png',
        'datatype': 'pyephem',
        'class': 'ephem.Mars()',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "jupiter": {
        'active': 1,
        'name': 'Jupiter',
        'category': 'planets',
        'color': 'lightblue',
        'symbol':'Jupiter_symbol.svg',
        'pic':'pic-jupiter.png',
        'datatype': 'pyephem',
        'class': 'ephem.Jupiter()',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "saturn": {
        'active': 1,
        'name': 'Saturn',
        'category': 'planets',
        'color': 'pink',
        'pic':'pic-saturn_2.png',
        'symbol':'Saturn_symbol.svg',
        'datatype': 'pyephem',
        'class': 'ephem.Saturn()',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "uranus": {
        'active': 1,
        'name': 'Uranus',
        'category': 'planets',
        'color': 'brown',
        'symbol':'Uranus_symbol.svg',
        'pic':'pic-uranus.png',
        'datatype': 'pyephem',
        'class': 'ephem.Uranus()',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "neptune": {
        'active': 1,
        'name': 'Neptun',
        'category': 'planets',
        'color': 'violett',
        'symbol':'Neptune_symbol.svg',
        'pic':'pic-neptune.png',
        'datatype': 'pyephem',
        'class': 'ephem.Neptune()',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
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
        'class': 'ephem.Moon()',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },    
    "iss": {
        'active': 1,
        'name': 'ISS (Internationale Raumstation)',
        'parsekey': 'ISS (ZARYA)',
        'category': 'earthsatellites',
        'color': '#ffffff',
        'symbol':'ISS_insignia.svg',
        'pic':'pic-iss.png',
        'datatype': 'tle',
        'sourcefile': 'data/tle/catalog.txt',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
        # or http://www.celestrak.com/NORAD/elements/amateur.txt
    },
    
#Raumsonden__Space-Probes_______________________________________________
    "voyager1": {
        'active': 1,
        'name': 'Voyager 1',
        'category': 'spaceprobes',
        'color': '#ffffff',
        'symbol':'Voyager_symbol.svg',
        'pic':'pic-voyager1.png',
        'datatype': 'nasacsv',
        'sourcefile': 'data/nasacsv/voyager_1.csv',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "voyager2": {
        'active': 1,
        'name': 'Voyager 2',
        'category': 'spaceprobes',
        'color': '#ffffff',
        'symbol':'Voyager_symbol.svg',
        'pic':'pic-voyager2.png',
        'datatype': 'nasacsv',
        'sourcefile': 'data/nasacsv/voyager_2.csv',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "hubble": {
        'active': 1,
        'name': 'Hubble Space Telescope',
        'parsekey': 'HST',
        'category': 'spaceprobes',
        'color': '#ffffff',
        'symbol':'Hubble_logo.svg',
        'pic':'pic-hubble.png',
        'datatype': 'tle',
        'sourcefile': 'data/tle/catalog.txt', 
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    
#Weltraumschrott__Space_Debris__________________________________________
    #Envisat
    "envisat": {
        'active': 1,
        'name': 'Envisat',
        'parsekey': 'ENVISAT',
        'category': 'spacedebris',
        'color': '#ffffff',
        'symbol':'Envisat.svg',
        'pic':'pic-envisat.png',
        'datatype': 'tle', 
        'sourcefile': 'data/tle/catalog.txt', # or http://www.celestrak.com/Norad/elements/visual.txt
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    #Vanguard 1
    "vanguard_1": {
        'active': 1,
        'name': 'Vanguard 1',
        'parsekey': 'VANGUARD 1',
        'category': 'spacedebris',
        'color': '#ffffff',
        'symbol':'Satellite2.svg',
        'pic':'pic-vanguard1.png',
        'datatype': 'tle',
        'sourcefile': 'data/tle/catalog.txt',
        'description': 'erster Solarbetriebener Satellit. <br/>1958 von der US Navy in den Orbit geschossen.<br/>Das &auml;lteste noch im Orbit befindliche Objekt'
    },
    #Cosmos 382 
    "cosmos_382": {
        'active': 1,
        'name': 'Cosmos 382',
        'parsekey': 'COSMOS 382',
        'category': 'spacedebris',
        'color': '#ffffff',
        'symbol':'Satellite.svg',
        'pic':'pic-cosmos_384.png',
        'datatype': 'tle',
        'sourcefile': 'data/tle/catalog.txt',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    #Kosmos 1818 
    "cosmos_1818": {
        'active': 1,
        'name': 'Cosmos 1818',
        'parsekey': 'COSMOS 1818',
        'category': 'spacedebris',
        'color': '#ffffff',
        'symbol':'Satellite.svg',
        'pic':'pic-cosmos_1818.png',
        'datatype': 'tle',
        'sourcefile': 'data/tle/catalog.txt',
        'description': '1.500Kg schwerer Spionagesatellit. 1987 vom<br/>russischen Baikonur Cosmodromevon in Orbit<br/>geschossen-eine Art fliegendes Tschernobyl<br/>'
    },
    
#Sterne___Stars_________________________________________________________
    "aldebaran": {
        'active': 1,
        'name': '- Tauri - Aldebaran',
        'category': 'stars',
        'color': '#ffffff',
        'symbol':'Alpha_symbol.svg',
        'pic':'pic-aldebaran-rund.png',
        'distance': '65ly',
        'datatype': 'pyephem',
        'class': 'ephem.star("Aldebaran")',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "antares": {
        'active': 1,
        'name': '- Scorpii - Antares',
        'category': 'stars',
        'color': '#ffffff',
        'symbol':'Alpha_symbol.svg',
        'pic':'pic-antares.png',
        'distance': '600ly',  
        'datatype': 'pyephem',
        'class': 'ephem.star("Antares")',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "sirius": {
        'active': 1,
        'name': '- Canis Majoris - Sirius',
        'category': 'stars',
        'color': '#ffffff',
        'symbol':'Alpha_symbol.svg',
        'pic':'pic-sirius.png',
        'distance': '8.60ly', # +- 0,04 
        'datatype': 'pyephem',
        'class': 'ephem.star("Sirius")',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "polaris": {
        'active': 1,
        'name': '- Ursae Minoris - Polaris ',
        'category': 'stars',
        'color': '#ffffff',
        'symbol':'Alpha_symbol.svg',
        'pic':'pic-polaris.png',
        'distance': '431ly', # +- 27
        'datatype': 'pyephem',
        'class': 'ephem.star("Polaris")',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "vega": {
        'active': 1,
        'name': 'Vega',
        'category': 'stars',
        'color': '#ffffff',
        'symbol':'Alpha_symbol.svg',
        'pic':'pic-vega.png', 
        'distance': '25.00ly', # +- 0,1
        'datatype': 'pyephem',
        'class': 'ephem.star("Vega")',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
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
        'distance': '-1',
        'datatype': 'pyephem', 
        'class': 'ephem.star("Schedar")',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
	#Southerncross -> using star Mimosa which is part of constellation
	"southerncross": {
        'active': 1,
        'name': 'S&uuml;dkreuz (Crux)',
        'category': 'constellations',
        'color': '#ffffff',
        'symbol':'Southerncross.svg',
        'pic':'pic-southerncross.png',
        'distance': '-1',
        'datatype': 'pyephem', 
        'class': 'ephem.star("Mimosa")',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
	#Big Bear or Das Reiterlein im grossen Wagen -> using star Megrez 
	"big_bear": {
        'active': 1,
        'name': 'Grosser B&auml;r (Ursa Major)',
        'category': 'constellations',
        'color': '#ffffff',
        'symbol':'Big_Bear-Ursa_Major.svg',
        'pic':'pic-big_bear-ursa_major.png',
        'distance': '-1', 
        'datatype': 'pyephem', 
        'class': 'ephem.star("Megrez")',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    #Orion -> using Betelgeuse
    "orion": {
        'active': 1,
        'name': 'Orion',
        'category': 'constellations',
        'color': '#ffffff',
        'symbol':'Orion_IAU.svg',
        'pic':'pic-orion.png',
        'distance': '-1',
        'datatype': 'pyephem', 
        'class': 'ephem.star("Betelgeuse")',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },

#Asteroiden___Asteroids_________________________________________________
    "243_Ida": {
        'active': 1,
        'name': '243 Ida',
        'category': 'asteroids',
        'color': '#ffffff',
        'symbol':'Asteroid.svg',
        'pic':'pic-243_ida.png',
        'datatype': 'nasacsv',
        'sourcefile': 'data/nasacsv/243_Ida.csv',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
    "2010_TK7": {
        'active': 1,
        'name': '2010 TK7',
        'category': 'asteroids',
        'color': '#ffffff',
        'symbol':'Asteroid.svg',
        'pic':'pic-2010_TK7.png',
        'datatype':  'nasacsv',
        'sourcefile': 'data/nasacsv/2010_TK7.csv',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
#Kometen___comets_______________________________________________________
	#Georges Perec
		#unknown
	#1P/Halley
    "halley": {
        'active': 1,
        'name': '1P/Halley',
        'category': 'comets',
        'color': '#ffffff',
        'symbol':'Comet.svg',
        'pic':'pic-halley.png',
        'datatype': 'nasacsv',
        'sourcefile': 'data/nasacsv/halley.csv',
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
	#ISON C/2012 S1 
    "ISON": {
        'active': 1,
        'name': 'ISON C/2012 S1',
        'category': 'comets',
        'color': '#ffffff',
        'symbol':'Comet.svg',
        'pic':'pic-ISON_C-2012.png',
        'datatype': 'nasacsv',
        'sourcefile': 'data/nasacsv/ISON.csv', 
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
	},
#Galaxien___Galaxies____________________________________________________
    #M 31 aka Andromeda Galaxy aka C/2002 Y1 (Juels-Holvorcem)
    #Data from http://www.maa.mhn.de/Tools/Xephem/Messier.edb
    "M31": {
        'active': 1,
        'name': 'M 31 - Andromeda',
        'category': 'galaxies',
        'color': '#ffffff',
        'symbol':'Galaxy.svg',
        'pic':'pic-M31.png',   
        'distance': '8.60ly', ##checkern     
        'datatype': 'pyephem',
        'class': 'ephem.readdb("M31,f|G,0:42:44,+41:16:8,4.16,2000,11433|3700|35")', 
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
    },
#Gegenerde___Globus_Cassus______________________________________________
	#Antichthon
	"antichthon": {
        'active': 1,
        'name': 'Antichthon',
        'category': 'globus_cassus',
        'color': '#ffff00',
        'symbol':'Antichthon.svg',
        'pic':'pic-antichthon.png', 
        'datatype': 'pyephem', # Same direction as the Sun
        'class': 'ephem.Sun()', 
        'description': 'Sample Description &auml;&ouml;&uuml; asd<br/>nl<br/>adlkj asd'
        },
}

