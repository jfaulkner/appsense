#! /usr/bin/python
import sys
import os
from gps import *
import time
import threading
from pymongo import MongoClient
 
gpsd = None #seting the global variable
gpsp = None
SAMPLE_RATE = 5 #set to a reasonable retry delay

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    global gpsp
    while gpsp.running:
      gpsd.next()

def getGpsData():
  global gpsp 
  gpsp = GpsPoller() # create the thread
  coords = {'lat':0.0,'lon':0.0,'utc':''}
  try:
    gpsp.start() # start it up
    while coords['lat']==0.0 or coords['lon']==0.0 or coords['utc']=='':
      # gps connection could take some time
      print('----------------------------------------')
      print(gpsd)
      coords['lat'] = gpsd.fix.latitude
      coords['lon'] = gpsd.fix.longitude
      coords['eps'] = gpsd.fix.eps
      coords['epx'] = gpsd.fix.epx
      coords['epv'] = gpsd.fix.epv
      coords['ept'] = gpsd.fix.ept
      coords['spd'] = gpsd.fix.speed
      coords['clm'] = gpsd.fix.climb
      coords['trk'] = gpsd.fix.track
      coords['mod'] = gpsd.fix.mode
      coords['sat'] = str(gpsd.satellites)
      coords['utc'] = gpsd.utc
      time.sleep(SAMPLE_RATE) 
    #print "\nKilling Thread..."
    print('----------------------------------------')
    print(coords)
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing 
  except (KeyboardInterrupt,SystemExit):
    #print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  return coords

def main():
  client = MongoClient('mongodb://localhost:27017')
  gpsdb = client.gpsdb
  collectionDate = time.strftime("%Y%m%d%H%M%S", time.gmtime())
  gpscol = gpsdb[str('trip'+collectionDate)]
  print("Starting.... %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())))
  while 0==0:
    gpsData = getGpsData()
    gpscol.insert(gpsData)
  print("Ending...")

if __name__ == '__main__':
    main()
