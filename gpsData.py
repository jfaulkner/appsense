#! /usr/bin/python
import sys
import os
from gps import *
import time
import threading
 
gpsd = None #seting the global variable
gpsp = None
SAMPLE_RATE = 2 #set to a reasonable retry delay
 
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

def getCoords():
  global gpsp 
  gpsp = GpsPoller() # create the thread
  coords = {'lat':0.0,'lon':0.0,'utc':''}
  try:
    gpsp.start() # start it up
    while coords['lat']==0.0 or coords['lon']==0.0 or coords['utc']=='':
      # gps connection could take some time
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      #os.system('clear')
 
      #print
      #print ' GPS reading'
      #print '----------------------------------------'
      #print 'latitude    ' , gpsd.fix.latitude
      #print 'longitude   ' , gpsd.fix.longitude
      #print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      #print 'altitude (m)' , gpsd.fix.altitude
      #print 'eps         ' , gpsd.fix.eps
      #print 'epx         ' , gpsd.fix.epx
      #print 'epv         ' , gpsd.fix.epv
      #print 'ept         ' , gpsd.fix.ept
      #print 'speed (m/s) ' , gpsd.fix.speed
      #print 'climb       ' , gpsd.fix.climb
      #print 'track       ' , gpsd.fix.track
      #print 'mode        ' , gpsd.fix.mode
      #print
      #print 'sats        ' , gpsd.satellites
      coords['lat'] = gpsd.fix.latitude
      coords['lon'] = gpsd.fix.longitude
      coords['utc'] = gpsd.utc
      time.sleep(SAMPLE_RATE) 
    #print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing 
  except (SystemExit):
    #print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  #print "latitude: "+str(coords['lat'])
  #print "longitude: "+str(coords['lon'])
  #print "time: "+str(coords['utc'])
  #print "Done.\nExiting."
  return coords

def main():
  print "Starting.... %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
  # use GPS data for message
  i=0
  while i<10:
    coords = getCoords()
    lat=str(coords['lat'])
    lon=str(coords['lon'])
    utc=str(coords['utc'])
    print "lat: " + lat
    print "lon: " + lon
    print "utc: " + utc
    i=i+1
  print "Ending..."

if __name__ == '__main__':
    main()
