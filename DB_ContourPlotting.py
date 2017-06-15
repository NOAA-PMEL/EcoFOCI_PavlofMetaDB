#!/usr/bin/env python

"""

 Background:
 --------
 DB_ContourPlotting.py
 
 Purpose:
 --------
 Various routines for visualizing ALAMO data

 History:
 --------

"""

#System Stack
import datetime
import argparse

import numpy as np
import pandas as pd

# Visual Stack
import matplotlib as mpl
mpl.use('Agg') 
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.dates import YearLocator, WeekdayLocator, MonthLocator, DayLocator, HourLocator, DateFormatter
import matplotlib.ticker as ticker
import cmocean

from io_utils.EcoFOCI_db_io import EcoFOCI_db_ProfileData

__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2016, 9, 22)
__modified__ = datetime.datetime(2016, 9, 22)
__version__  = "0.1.0"
__status__   = "Development"
__keywords__ = 'ctd','FOCI'

mpl.rcParams['axes.grid'] = False
mpl.rcParams['axes.edgecolor'] = 'white'
mpl.rcParams['axes.linewidth'] = 0.25
mpl.rcParams['grid.linestyle'] = '--'
mpl.rcParams['grid.linestyle'] = '--'
mpl.rcParams['xtick.major.size'] = 2
mpl.rcParams['xtick.minor.size'] = 1
mpl.rcParams['xtick.major.width'] = 0.25
mpl.rcParams['xtick.minor.width'] = 0.25
mpl.rcParams['ytick.major.size'] = 2
mpl.rcParams['ytick.minor.size'] = 1
mpl.rcParams['xtick.major.width'] = 0.25
mpl.rcParams['xtick.minor.width'] = 0.25
mpl.rcParams['ytick.direction'] = 'out'
mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['ytick.color'] = 'grey'
mpl.rcParams['xtick.color'] = 'grey'
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['svg.fonttype'] = 'none'

# Example of making your own norm.  Also see matplotlib.colors.
# From Joe Kington: This one gives two different linear ramps:

class MidpointNormalize(colors.Normalize):
	def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
		self.midpoint = midpoint
		colors.Normalize.__init__(self, vmin, vmax, clip)

	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y))

"""----------------------------- Main -------------------------------------"""

parser = argparse.ArgumentParser(description='ArcticHeat ctd datafile parser ')
parser.add_argument('filepath', metavar='filepath', type=str,
			   help='full path to file')
parser.add_argument('--maxdepth', type=float, default=70, 
	help="known bathymetric depth at location")
parser.add_argument('--paramspan', nargs='+', type=float, 
	help="max,min of parameter")
parser.add_argument('-cruiseid','--cruiseid', type=str,
	help='work with alamo float data in sql database')
parser.add_argument('-castno','--castno', type=int, nargs=2,
	help='start and stop range for cast number')
parser.add_argument('-plot_cbz','--plot_cb_zero', type=float, 
	help='Colorbar inflection value for divergent color scheme')
parser.add_argument('-time','--time', action="store_true",
	help='create a contour plot with time as the x-axis')
parser.add_argument('-distance','--distance', action="store_true",
	help='create a contour plot with distance as the x-axis')
args = parser.parse_args()


if args.time:

	startcycle=args.castno[0]
	endcycle=args.castno[1]

	#get information from local config file - a json formatted file
	config_file = 'EcoFOCI_config/db_config/db_config_profiledata.pyini'


	EcoFOCI_db = EcoFOCI_db_ProfileData()
	(db,cursor) = EcoFOCI_db.connect_to_DB(db_config_file=config_file)

	depth_array = np.arange(0,args.maxdepth+1,0.5) 
	num_cycles = EcoFOCI_db.count(table=args.cruiseid, start='ctd'+str(startcycle).zfill(3), end='ctd'+str(endcycle).zfill(3), verbose=True)
	temparray = np.ones((num_cycles,len(depth_array)))*np.nan
	ProfileTime = []
	cycle_col=0

	fig = plt.figure(1, figsize=(12, 3), facecolor='w', edgecolor='w')
	ax1 = fig.add_subplot(111)		
	for cycle in range(startcycle,endcycle+1,1):
		#get db meta information for mooring
		cyclestr = 'ctd'+str(cycle).zfill(3)
		Profile = EcoFOCI_db.read_profile(table=args.cruiseid, ProfileID=cyclestr, verbose=True)

		#try:
		temp_time =  Profile[sorted(Profile.keys())[0]]['ProfileTime']
		ProfileTime = ProfileTime + [temp_time]
		Pressure = np.array(sorted(Profile.keys()))
		Temperature = np.array([Profile[x]['T_28'] for x in sorted(Profile.keys()) ])
		#Temperature[Temperature<30.] = np.nan

		temparray[cycle_col,:] = np.interp(depth_array,Pressure,Temperature,left=np.nan,right=np.nan)
		cycle_col +=1

		xtime = np.ones_like(np.array(sorted(Profile.keys()))) * mpl.dates.date2num(temp_time)
		#turn off below and set zorder to 1 for no scatter plot colored by points
		plt.scatter(x=xtime, y=np.array(sorted(Profile.keys())),s=1,marker='.', edgecolors='none', c='k', zorder=3, alpha=1) 
		
		plt.scatter(x=xtime, y=np.array(sorted(Profile.keys())),s=15,marker='.', edgecolors='none', c=Temperature, 
		vmin=args.paramspan[0], vmax=args.paramspan[1], 
		cmap=cmocean.cm.thermal, zorder=1)
		#except IndexError:
		#	pass


	cbar = plt.colorbar()
	cbar.set_label('Temperature (C)',rotation=0, labelpad=90)
	plt.contourf(ProfileTime,depth_array,temparray.T, 
		extend='both', cmap=cmocean.cm.thermal, levels=np.arange(args.paramspan[0],args.paramspan[1],0.25), alpha=1.0)

	ax1.invert_yaxis()
	ax1.xaxis.set_major_locator(DayLocator(bymonthday=15))
	ax1.xaxis.set_minor_locator(DayLocator(interval=1))
	ax1.xaxis.set_major_formatter(ticker.NullFormatter())
	ax1.xaxis.set_minor_formatter(DateFormatter('%d'))
	ax1.xaxis.set_major_formatter(DateFormatter('%b %y'))
	ax1.xaxis.set_tick_params(which='major', pad=25)

	plt.tight_layout()
	plt.savefig(args.filepath + '_time.svg', transparent=False, dpi = (300))
	plt.savefig(args.filepath + '_time.png', transparent=False, dpi = (300))
	plt.close()

if args.distance:

	startcycle=args.castno[0]
	endcycle=args.castno[1]

	#get information from local config file - a json formatted file
	config_file = 'EcoFOCI_config/db_config/db_config_profiledata.pyini'


	EcoFOCI_db = EcoFOCI_db_ProfileData()
	(db,cursor) = EcoFOCI_db.connect_to_DB(db_config_file=config_file)

	depth_array = np.arange(0,args.maxdepth+1,0.5) 
	num_cycles = EcoFOCI_db.count(table=args.cruiseid, start='ctd'+str(startcycle).zfill(3), end='ctd'+str(endcycle).zfill(3), verbose=True)
	temparray = np.ones((num_cycles,len(depth_array)))*np.nan
	ProfileTime = []
	cycle_col=0

	fig = plt.figure(1, figsize=(12, 3), facecolor='w', edgecolor='w')
	ax1 = fig.add_subplot(111)		
	for cycle in range(startcycle,endcycle+1,1):
		#get db meta information for mooring
		cyclestr = 'ctd'+str(cycle).zfill(3)
		Profile = EcoFOCI_db.read_profile(table=args.cruiseid, ProfileID=cyclestr, verbose=True)

		if cycle == startcycle:
			ref_lat = Profile[sorted(Profile.keys())[0]]['lat']
			ref_lon = Profile[sorted(Profile.keys())[0]]['lon']
		#try:
		distance = EcoFOCI_db.get_distance(ref_lat, ref_lon, Profile[sorted(Profile.keys())[0]]['id'])
		ProfileTime = ProfileTime + [distance]
		Pressure = np.array(sorted(Profile.keys()))
		Temperature = np.array([Profile[x]['T_28'] for x in sorted(Profile.keys()) ])
		#Temperature[Temperature<30.] = np.nan

		temparray[cycle_col,:] = np.interp(depth_array,Pressure,Temperature,left=np.nan,right=np.nan)
		cycle_col +=1

		xtime = np.ones_like(np.array(sorted(Profile.keys()))) * distance
		#turn off below and set zorder to 1 for no scatter plot colored by points
		plt.scatter(x=xtime, y=np.array(sorted(Profile.keys())),s=1,marker='.', edgecolors='none', c='k', zorder=3, alpha=1) 
		
		plt.scatter(x=xtime, y=np.array(sorted(Profile.keys())),s=15,marker='.', edgecolors='none', c=Temperature, 
		vmin=args.paramspan[0], vmax=args.paramspan[1], 
		cmap=cmocean.cm.thermal, zorder=1)
		#except IndexError:
		#	pass


	cbar = plt.colorbar()
	cbar.set_label('Temperature (C)',rotation=0, labelpad=90)
	plt.contourf(ProfileTime,depth_array,temparray.T, 
		extend='both', cmap=cmocean.cm.thermal, levels=np.arange(args.paramspan[0],args.paramspan[1],0.25), alpha=0.8)

	ax1.invert_yaxis()


	plt.tight_layout()
	plt.savefig(args.filepath + '_dist.svg', transparent=False, dpi = (300))
	plt.savefig(args.filepath + '_dist.png', transparent=False, dpi = (300))
	plt.close()