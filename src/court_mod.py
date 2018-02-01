#!/usr/bin/env python
#####################################
# court_mod.py
#   plot court dimensions
#
# Jason Chang
# December 2015
######################################
  
  
###################################
# imports
###################################
import matplotlib.pyplot as plot
import matplotlib.lines  as lines
import math
import numpy as np
  
  
###################################
# create court
###################################
def plot_court(fig):
  ### court dimensions ###
  # boundaries
  edge_xll = 0.
  edge_xur = 94.
  edge_yll = 0.
  edge_yur = 50.
  # centercourt
  center_r1 = 6.
  center_r2 = 2.
  # key
  key_x    = 18.333
  key_outy = 16.
  key_iny  = 12.
  key_r    = 6.
  # three
  three_x = 14.
  three_y = 3.
  three_r = 23.75
  three_a = 0.123
  # basket
  back_x = 4.
  back_y = 6.
  cyl_x  = 5.25
  cyl_r  = 0.75
  # restricted
  rstr_r = 4.
  
  
  ### court line style ###
  # style
  ecol = 'k-'
  bcol = 'b-'
  lw  = 4
  bw  = 2
  
  
  ### edges ###
  plot.plot((edge_xll,edge_xll),(edge_yll,edge_yur),ecol,linewidth=lw,zorder=1)
  plot.plot((edge_xur,edge_xur),(edge_yll,edge_yur),ecol,linewidth=lw,zorder=1)
  plot.plot((edge_xll,edge_xur),(edge_yll,edge_yll),ecol,linewidth=lw,zorder=1)
  plot.plot((edge_xll,edge_xur),(edge_yur,edge_yur),ecol,linewidth=lw,zorder=1)
  plot.plot((edge_xur/2.,edge_xur/2.),(edge_yll,edge_yur),ecol,linewidth=lw,zorder=1)

  
  ### west key ###
  # outer key
  key_xll  = 0
  key_xur  = key_x
  key_yll  = (edge_yur/2.)-(key_outy/2.)
  key_yur  = (edge_yur/2.)+(key_outy/2.)
  plot.plot((key_xll,key_xur),(key_yll,key_yll),ecol,linewidth=lw,zorder=1)
  plot.plot((key_xll,key_xur),(key_yur,key_yur),ecol,linewidth=lw,zorder=1)
  plot.plot((key_xur,key_xur),(key_yll,key_yur),ecol,linewidth=lw,zorder=1)
  # inner key
  key_xll  = 0
  key_xur  = key_x
  key_yll  = (edge_yur/2.)-(key_iny/2.)
  key_yur  = (edge_yur/2.)+(key_iny/2.)
  plot.plot((key_xll,key_xur),(key_yll,key_yll),ecol,linewidth=lw,zorder=1)
  plot.plot((key_xll,key_xur),(key_yur,key_yur),ecol,linewidth=lw,zorder=1)
  
  
  ### east key ###
  # outer key
  key_xll  = edge_xur-key_x
  key_xur  = edge_xur
  key_yll  = (edge_yur/2.)-(key_outy/2.)
  key_yur  = (edge_yur/2.)+(key_outy/2.)
  plot.plot((key_xll,key_xur),(key_yll,key_yll),ecol,linewidth=lw,zorder=1)
  plot.plot((key_xll,key_xur),(key_yur,key_yur),ecol,linewidth=lw,zorder=1)
  plot.plot((key_xll,key_xll),(key_yll,key_yur),ecol,linewidth=lw,zorder=1)
  # inner key
  key_xll  = edge_xur-key_x
  key_xur  = edge_xur
  key_yll  = (edge_yur/2.)-(key_iny/2.)
  key_yur  = (edge_yur/2.)+(key_iny/2.)
  plot.plot((key_xll,key_xur),(key_yll,key_yll),ecol,linewidth=lw,zorder=1)
  plot.plot((key_xll,key_xur),(key_yur,key_yur),ecol,linewidth=lw,zorder=1)
  
  
  ### circles: west key ###
  circ_x = key_x
  circ_y = edge_yur/2.
  key_w = plot.Circle((circ_x,circ_y),key_r,fill=False,linewidth=lw,zorder=1)
  fig.gca().add_artist(key_w)
  
  
  ### circles: east key ###
  circ_x = edge_xur-key_x
  circ_y = edge_yur/2.
  key_e = plot.Circle((circ_x,circ_y),key_r,fill=False,linewidth=lw,zorder=1)
  fig.gca().add_artist(key_e)
  
  
  ### circles: midcourt ###
  circ_x = edge_xur/2.
  circ_y = edge_yur/2.
  center = plot.Circle((circ_x,circ_y),center_r1,fill=False,linewidth=lw,zorder=1)
  fig.gca().add_artist(center)
  center = plot.Circle((circ_x,circ_y),center_r2,fill=False,linewidth=lw,zorder=1)
  fig.gca().add_artist(center)
  
  
  ### west three point line ###
  # corners
  three_xll = 0.
  three_xur = three_x
  three_yll = three_y
  three_yur = edge_yur-three_y
  plot.plot((three_xll,three_xur),(three_yll,three_yll),ecol,linewidth=lw,zorder=1)
  plot.plot((three_xll,three_xur),(three_yur,three_yur),ecol,linewidth=lw,zorder=1)
  # arc
  angles = np.linspace(-(math.pi/2.-three_a*math.pi),(math.pi/2.-three_a*math.pi),50)
  trey_x = three_r*np.cos(angles)+(edge_xll+cyl_x)
  trey_y = three_r*np.sin(angles)+(edge_yur/2.)
  plot.plot(trey_x,trey_y,ecol,linewidth=lw,zorder=1)
  
  
  ### east three point line ###
  # corners
  three_xll = edge_xur-three_x
  three_xur = edge_xur
  three_yll = three_y
  three_yur = edge_yur-three_y
  plot.plot((three_xll,three_xur),(three_yll,three_yll),ecol,linewidth=lw,zorder=1)
  plot.plot((three_xll,three_xur),(three_yur,three_yur),ecol,linewidth=lw,zorder=1)
  # arc
  angles = np.linspace((math.pi/2.+three_a*math.pi),(3*math.pi/2.-three_a*math.pi),50)
  trey_x = three_r*np.cos(angles)+(edge_xur-cyl_x)
  trey_y = three_r*np.sin(angles)+(edge_yur/2.)
  plot.plot(trey_x,trey_y,ecol,linewidth=lw,zorder=1)
  
  
  ### west basket ###
  # backboard
  back_xll = back_x
  back_xur = back_x
  back_yll = (edge_yur/2.)-(back_y/2.)
  back_yur = (edge_yur/2.)+(back_y/2.)
  plot.plot((back_xll,back_xur),(back_yll,back_yur),bcol,linewidth=lw,zorder=1)
  # basket
  basket_x = cyl_x
  basket_y = edge_yur/2.
  center = plot.Circle((basket_x,basket_y),cyl_r,color='b',fill=False,linewidth=bw,zorder=1)
  fig.gca().add_artist(center)
  
  
  ### east basket ###
  # backboard
  back_xll = edge_xur-back_x
  back_xur = edge_xur-back_x
  back_yll = (edge_yur/2.)-(back_y/2.)
  back_yur = (edge_yur/2.)+(back_y/2.)
  plot.plot((back_xll,back_xur),(back_yll,back_yur),bcol,linewidth=lw,zorder=1)
  # basket
  basket_x = edge_xur-cyl_x
  basket_y = edge_yur/2.
  center = plot.Circle((basket_x,basket_y),cyl_r,color='b',fill=False,linewidth=bw,zorder=1)
  fig.gca().add_artist(center)
  
  
  ### west restricted zone ###
  angles = np.linspace(-math.pi/2.,math.pi/2.,50)
  rstr_x = rstr_r*np.cos(angles)+(edge_xll+cyl_x)
  rstr_y = rstr_r*np.sin(angles)+(edge_yur/2.)
  plot.plot(rstr_x,rstr_y,bcol,linewidth=lw,zorder=1)
  
  
  ### east restricted zone ###
  angles = np.linspace(math.pi/2.,3*math.pi/2.,50)
  rstr_x = rstr_r*np.cos(angles)+(edge_xur-cyl_x)
  rstr_y = rstr_r*np.sin(angles)+(edge_yur/2.)
  plot.plot(rstr_x,rstr_y,bcol,linewidth=lw,zorder=1)
