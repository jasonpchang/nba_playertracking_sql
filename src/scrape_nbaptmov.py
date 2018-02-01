#!/usr/bin/env python
###############################################
# scrape_nbaptmov.py
#
# python code to grab player movement data from online json
# converts data to local sql database
###############################################

#################################
# imports and aliases
#################################
import sys
import re
import os
import sqlite3
import load_movement_mod as mm
#import load_playbyplay_mod as pbp



#################################
# kernel
#################################
### check number of arguments ###
if (len(sys.argv) < 5):
  print "Usage:"
  print "     %s [begin date] [end date] [name of db] [prompt?]" %(sys.argv[0])
  print "     date format: mm-dd-yyyy"
  sys.exit()

### grab variables ###
bdate  = sys.argv[1]
edate  = sys.argv[2]
dbname = sys.argv[3]
in5    = int(sys.argv[4])
if (in5 == 0):
  prompt = False
else:
  prompt = True

### parse beginning and end dates ###
date = re.compile("^(\d\d)-(\d\d)-(\d\d\d\d)$")
find = date.search(bdate)
if (find):
  bmonth = find.group(1)
  bday   = find.group(2)
  byear  = find.group(3)
else:
  print "Start date format does not work"
  sys.exit()
bdate = int('%s%s%s' %(byear,bmonth,bday))
find = date.search(edate)
if find:
  emonth = find.group(1)
  eday   = find.group(2)
  eyear  = find.group(3)
else:
  print "End date format does not work"
  sys.exit()
edate = int('%s%s%s' %(eyear,emonth,eday))
# check that dates make sense
if edate<bdate:
  print "Need begin date to be earlier than end date"
  sys.exit()

### touch sqlite3 database ###
if os.path.isfile(dbname):
  db  = sqlite3.connect(dbname)
  hdb = db.cursor()
else:
  db  = sqlite3.connect(dbname)
  hdb = db.cursor()
  mm.movement_init(hdb)
  #pbp.playbyplay_init(hdb)

### add information to database ###
mm.movement_add_info(hdb,bdate,edate,prompt)
#pbp.playbyplay_add_info(hdb,bdate,edate,prompt)

### clean up ###
db.commit()
db.close()
