#!/usr/bin/env

"""
 EcoRAIDMooringMetaData2ptr.py
 
 Purpose:
 --------

 Generate pointer files for EcoFOCI data housed on EcoRAID

 History:
 --------


"""

import os
import sys
import datetime

import argparse

#User Stack
from io_utils.EcoFOCI_db_io import EcoFOCI_db_datastatus

__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2016, 8, 20)
__modified__ = datetime.datetime(2016, 8, 20)
__version__  = "0.1.0"
__status__   = "Development"


"""------------------------------------------------------------------------------------"""
parser = argparse.ArgumentParser(description='MySQL database --> .ptr file')
parser.add_argument('SiteID', metavar='SiteID', type=str,
	help='Base Site ID')
parser.add_argument('year', metavar='datatype', type=int,
	help="year")
parser.add_argument('MooringID', metavar='MooringID', nargs='+', type=str,
	help='list of mooring ids')

args = parser.parse_args()


EcoFOCI_db = EcoFOCI_db_datastatus()
config_file = '/Volumes/WDC_internal/Users/bell/Programs/Python/db_connection_config_files/db_config_datastatus.pyini'
(db,cursor) = EcoFOCI_db.connect_to_DB(db_config_file=config_file)

for MooringSite in args.MooringID:
	data = EcoFOCI_db.read_table(table='ecoraid_filemetainfo',
								 mooringid=MooringSite,
								 year=args.year)

	for k in data.keys():
		if data[k]['isfinaldata'] == 'y':
			print "{year}/Moorings/{mooringid}/final_data/{filename}".format(year=data[k]['year'],
																mooringid=data[k]['mooringid'],
																filename=data[k]['filenamefinal'])
		elif data[k]['isinitialarchive'] == 'y':
			print "{year}/Moorings/{mooringid}/initial_archive/{filename}".format(year=data[k]['year'],
																mooringid=data[k]['mooringid'],
																filename=data[k]['filenameinitial'])
		if data[k]['isspecialarchive'] == 'y':
			print "{year}/Moorings/{mooringid}/final_data/{filename}".format(year=data[k]['year'],
																mooringid=data[k]['mooringid'],
																filename=data[k]['filenameinitial'])
