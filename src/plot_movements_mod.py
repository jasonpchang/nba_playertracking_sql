#!/usr/bin/env python
############################################
# plot_movements_mod.py
#   module to plot movement data
###########################################


#################################
# imports
#################################
import matplotlib.pyplot as plot
import numpy as np
import sqlite3
import court_mod as court


#################################
# plot movement information
#################################
def plot_movements(hdb):
  # load movements
  gid = "0021400004"
  movements = []
  for movement in hdb.execute('SELECT * FROM movements WHERE game_id=%s ORDER BY event_id,team_id' %(gid)):
    movements.append(movement)
  #print movements[-1100:-1000]

  # convert to numpy array
  ms = np.asarray(movements)

  # check dimensions of information
  nvals = 11
  nframes = ms.shape[0]/float(nvals)
  print "Number of entries: %s" %(nframes)
  if (ms.shape[0]%float(nvals) != 0):
    print "Number of entries not divisible by 11"
  nframes = int(nframes)

  # create color dictionary
  cdict = {}
  teams = list(set(ms[:,5]))
  teams.sort()
  cdict['%s' %(teams[0])] = 'black'
  cdict['%s' %(teams[1])] = 'red'
  cdict['%s' %(teams[2])] = 'blue'
  # determine which colors to use
  cc = list(ms[:,5])
  col = []
  for color in cc:
    col.append(cdict['%s' %(color)])

  # plot player movement
  # figure dimensions
  plot.ion()
  scale  = 4.
  buff   = 0.5
  width  = (94/scale)+2*buff
  height = (50/scale)+2*buff
  fig = plot.figure(figsize=(width,height))
  for frame in range(nframes-100,nframes,1):
  #for frame in range(0,nframes,1):
    plot.xlim([0-(buff*scale),94+(buff*scale)])
    plot.ylim([0-(buff*scale),50+(buff*scale)])
    plot.gca().invert_yaxis()
    # plot first time steps
    ibeg = frame*nvals
    iend = (frame+1)*nvals
    x = ms[ibeg:iend,7]
    y = ms[ibeg:iend,8]
    color = col[ibeg:iend]
    # plot court
    court.plot_court(fig)
    # plot movements
    plot.scatter(x,y,c=color,s=500,zorder=2)
    # plot
    plot.draw()
    plot.pause(0.01)
    plot.clf()
