#!/usr/bin/env python

"""
 EcoFOCI_NetCDF2DB.py
 
 Input: MooringID (eg. 14bsm2a or 14BSM-2A)
 Output: text file with...
    mooring charactersistcs
    instruments deployed, depths, serial numbers

"""

# Standard library.
import datetime
import sys

# System Stack
import argparse

#User Stack
import io_utils.ConfigParserLocal as ConfigParserLocal
from calc.EPIC2Datetime import EPIC2Datetime
from io_utils.EcoFOCI_db_io import EcoFOCI_db_ProfileData
from io_utils.EcoFOCI_netCDF_read import EcoFOCI_netCDF


__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2017, 6, 13)
__modified__ = datetime.datetime(2017, 6, 13)
__version__  = "0.1.0"
__status__   = "Development"

"""------------------------------- lat/lon ----------------------------------------"""

def latlon_convert(Mooring_Lat, Mooring_Lon):
    
    tlat = Mooring_Lat.strip().split() #deg min dir
    lat = float(tlat[0]) + float(tlat[1]) / 60.
    if tlat[2] == 'S':
        lat = -1 * lat
        
    tlon = Mooring_Lon.strip().split() #deg min dir
    lon = float(tlon[0]) + float(tlon[1]) / 60.
    if tlon[2] == 'E':
        lon = -1 * lon
        
    return (lat, lon)
"""------------------------------- MAIN ----------------------------------------"""

parser = argparse.ArgumentParser(description='SBE mooring report')
parser.add_argument('ctd_file', metavar='ctd_file', type=str, help='Path to CTD file')               
parser.add_argument('-db', '--db_ini', type=str, help='path to db .pyini file')               
parser.add_argument('-c', '--create_table',  action="store_true", help='create new table')               
parser.add_argument('-f', '--isfinal',  action="store_true", help='flag if final data')               

args = parser.parse_args()
    
#get information from local config file - a json formatted file
if args.db_ini:
    config_file = args.db_ini
else:
    config_file = 'EcoFOCI_config/db_config/db_config_profiledata.pyini'

if args.isfinal:
    DataStatus='final'
else:
    DataStatus = 'preliminary'

#read in netcdf data file
df = EcoFOCI_netCDF(args.ctd_file)
global_atts = df.get_global_atts()
vars_dic = df.get_vars()
data = df.ncreadfile_dic()
df.close()

dt_from_epic =  EPIC2Datetime(data['time'], data['time2'])
str_time = dt_from_epic[0].strftime('%Y-%m-%d %H:%M:%S')

if args.create_table:
    EcoFOCI_db = EcoFOCI_db_ProfileData()
    (db,cursor) = EcoFOCI_db.connect_to_DB(db_config_file=config_file)

    EcoFOCI_db.create_table(tablename=global_atts['CRUISE'], vars_list=vars_dic.keys())

    EcoFOCI_db.close()
else:
    EcoFOCI_db = EcoFOCI_db_ProfileData()
    (db,cursor) = EcoFOCI_db.connect_to_DB(db_config_file=config_file)

    EcoFOCI_db.add_ctd_profile(tablename=global_atts['CRUISE'], 
                                castno=global_atts['CAST'], 
                                data=data, 
                                datetime=str_time,
                                DataStatus=DataStatus)

    EcoFOCI_db.close()