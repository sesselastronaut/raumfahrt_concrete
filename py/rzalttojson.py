
'''
version 0.1

outputs a list of celestial bodies as json file
to be interpreted by the web interface 

created: 2012-12-14 flx
'''
from config import *
import os
try:
    import json
except:
    import simplejson as json
import ephem
from ephem import *
import math
import datetime
from tle_parser import tle_parser

### defs 
ly2au = 63241.1
coords = {}
def dist2au(dist):
    global ly2au
    if dist.find('ly') != -1:
        return ly2au*float(dist[0:dist.find('ly')])
    
def fillArr(obj,meta,id):
    global coords
    if meta['datatype'] == 'nasacsv':# is nasa csv parsed
        size = 0.0001
        az = (math.pi/180)*float(obj['azi'])
        alt = (math.pi/180)*float(obj['elev'])
    else:
        size = obj.size
        az = obj.az
        alt = obj.alt
        
    if not id in coords:
        #print "add key",id
        coords[id] = {
            'category':meta['category'],
            'id':id,
            'name':meta['name'],
            'size':float(size),
            'color':meta['color'],
            'data':[]
            }
        if 'symbol' in meta:
            coords[id]['symbol'] = meta['symbol']
        if 'pic' in meta:
            coords[id]['pic'] = meta['pic']
            
        if(meta['datatype'] == 'nasacsv'):
            coords[id]['dist'] = obj['delta']
        elif(type(obj) == ephem.FixedBody):
            coords[id]['dist'] = dist2au(meta['distance'])
        elif(type(obj) == ephem.EarthSatellite):
            coords[id]['dist'] = obj.elevation/ephem.meters_per_au
        else:
            if id=='antichton':
                coords[id]['dist'] = obj.earth_distance*2
            else:
                coords[id]['dist'] = obj.earth_distance
            
    #test if difference to last angle is markable
    diff = 10
    if len(coords[id]['data']) != 0:
        lastAz = coords[id]['data'][len(coords[id]['data'])-1]['az']
        lastAlt = coords[id]['data'][len(coords[id]['data'])-1]['alt']
        diff = max(abs(float(az)-lastAz),abs(float(alt)-lastAlt))
    if diff > math.pi/36:
        if(type(obj) == ephem.EarthSatellite):
            coords[id]['data'].append({'az':float(az),'alt':float(alt)})#/ephem.meters_per_au
        else:
            coords[id]['data'].append({'az':float(az),'alt':float(alt)})
      
### app  


if __name__ == '__main__':
    
    # setup observer for ephem bodies
    # todo: check if gmt date for observer is correct
    obs = eval(OBSERVER)
    datenow = obs.date
    
    #print "set observer to:",obs.name,"date:",obs.date
    
    for b in CELESTIAL_BODY:
        body = None
        if CELESTIAL_BODY[b] and CELESTIAL_BODY[b]['active']:
            if CELESTIAL_BODY[b]['datatype'] == 'pyephem':
                body = eval(CELESTIAL_BODY[b]["class"])
            elif CELESTIAL_BODY[b]['datatype'] == 'tle':
                tle_file = open(CELESTIAL_BODY[b]["sourcefile"])
                #print b
                #print "tle file:"
                #print tle_file
                data_headline,data_row_1,data_row_2 = tle_parser.get_tle_data(tle_file, CELESTIAL_BODY[b]["parsekey"])
                #print "TLE data for readtle:"
                #print data_headline,data_row_1,data_row_2
                body = ephem.readtle(
                    data_headline,
                    data_row_1,
                    data_row_2
                    )
                tle_file.close()
            elif CELESTIAL_BODY[b]['datatype'] == 'nasacsv':
                startDate = datetime.datetime.now().strftime("%Y-%h-%d %H:%M")
                endDate = ephem.localtime( ephem.Date( datenow+RZALT_TIMESPAN_HOURS*ephem.hour ) ).strftime("%Y-%h-%d %H:%M")
                reading = 0
                f = open(os.getcwd()+'/'+CELESTIAL_BODY[b]["sourcefile"], 'r')
                for line in f:
                    if reading==0 and line.find(startDate) != -1:
                        #print "found start!"
                        reading=1
                    if reading==1:
                        if line.find(endDate) != -1:
                            #print "found stop!"
                            break;
                        line = line.split(",")
                        line = map(lambda l: l.strip(), line)
                        line = {"name":b, "date":line[0], "azi":line[3], "elev":line[4], "delta":line[5], "deldot":line[6]}
                        fillArr(line,CELESTIAL_BODY[b],b)
                f.close();
            #else:
                #print "nope",b
            # add ephem body to array
            if body:
                for i in range(0,60*(60/4)*RZALT_TIMESPAN_HOURS+1):
                    obs.date = datenow+i*(ephem.second*4)
                    body.compute(obs)
                    fillArr(body,CELESTIAL_BODY[b],b)

    # output json array 
    jsn = 'var arr='+json.dumps(coords)+';var cats='+json.dumps(CELESTIAL_BODY_CATEGORIES)
    if RZALT_JSON_OUTPUT == 'file':
        f = open(RZALT_JSON_FILE, 'w')
        f.write(jsn)
        f.close()
    else:
        print jsn
        

