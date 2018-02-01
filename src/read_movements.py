#!/usr/bin/env python
############################################
# read_movements.py
#
# inputs:
#   1) database name
#
# options:
#   1) plot player movements
###########################################


#################################
# imports
#################################
import matplotlib.pyplot as plot
import plot_movements_mod as plot_movements
#import heat_maps_mod as heat_maps
#import distance_mod as distance
import sqlite3
import sys
import os


#################################
# kernel
#################################
### check number of arguments ###
if (len(sys.argv) < 2):
  print "Usage:"
  print "	%s [database]" %(sys.argv[0])
  sys.exit()

### grab variables ###
dbname = sys.argv[1]

### touch sqlite3 database ###
if (os.path.isfile(dbname)):
  db  = sqlite3.connect(dbname)
  hdb = db.cursor()
else:
  print "Database does not exist"
  sys.exit()


### go through the options ###
opts = [1,2,3]
print "==================================="
print "Options:"
print "  (01) plot movements"
print "  (02) heat maps"
print "  (03) distance tracker"
print "==================================="
opt = int(raw_input('Select option: '))
while (opt not in opts):
  opt = int(raw_input('Choose option that exists: '))
print "==================================="


### go through the options ###
if (opt==1):
  # print something to the command line
  # need to have options for different games, period, etc
  print "Entering plotting movements..."
  plot_movements.plot_movements(hdb)
elif (opt==2):
  print 'Entering heat maps...'
  #heat_maps.location_map(hdb)
elif (opt==3):
  print 'Entering distance tracker...'
  #distance.parse_distance(hdb)
sys.exit()
