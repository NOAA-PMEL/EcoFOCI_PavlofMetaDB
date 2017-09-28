#!/usr/bin/env python

"""
SQL2GEOJSON_Moorings.py
 
export all mooring locations to geojson format for plotting


"""

#System Stack
import datetime
import argparse
import mysql.connector
import sys

#Science Stack
import numpy as np

#User Stack
import io_utils.ConfigParserLocal as ConfigParserLocal
from io_utils.EcoFOCI_db_io import EcoFOCI_db_datastatus


__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2015, 05, 28)
__modified__ = datetime.datetime(2015, 05, 28)
__version__  = "0.1.0"
__status__   = "Development"
__keywords__ = 'moorings','csv','google maps', 'heatmap', 'geojson'

"""------------------------------- MAIN ----------------------------------------"""

parser = argparse.ArgumentParser(description='Mooring Database -> GEOJSON For currently deployed')
parser.add_argument('--geojson', action='store_true', help='create geojson file')
parser.add_argument('--google_earth', action='store_true', help='create google earth file')
parser.add_argument('--all', action='store_true', help='create files for all moorings')

args = parser.parse_args()

#get information from local config file - a json formatted file
config_file = 'EcoFOCI_config/db_config/db_config_mooring.yaml'


EcoFOCI_db = EcoFOCI_db_datastatus()
(db,cursor) = EcoFOCI_db.connect_to_DB(db_config_file=config_file,ftype='yaml')

if args.all:
    data_mooring = EcoFOCI_db.read_mooring_summary(table='mooringdeploymentlogs')
else:
    data_mooring = EcoFOCI_db.read_mooring_summary(table='mooringdeploymentlogs',deployed=True,verbose=False)

#find missing or undeployed data and skip
for a_ind in data_mooring.keys():
    if (data_mooring[a_ind]['Latitude'] == '') or (data_mooring[a_ind]['Latitude'] == 'NOT DEPLOYED') or not(data_mooring[a_ind]['Latitude']):
        data_mooring[a_ind]['Latitude'] = '00 0.00 N'
        data_mooring[a_ind]['Longitude'] = '00 0.00 W'
    print data_mooring[a_ind]['Latitude'], data_mooring[a_ind]['Longitude']

mooring_lat = np.array([float(data_mooring[a_ind]['Latitude'].split()[0]) + float(data_mooring[a_ind]['Latitude'].split()[1])/60.0 for a_ind in data_mooring.keys()])
mooring_lon = np.array([-1.0*(float(data_mooring[a_ind]['Longitude'].split()[0]) + float(data_mooring[a_ind]['Longitude'].split()[1])/60.0) for a_ind in data_mooring.keys()])
mooringid = data_mooring.keys()

if args.geojson:
    ### "Generating .geojson"
    geojson_header = (
        '{"type": "FeatureCollection","features": ['
        )
    geojson_point_coords = ''

    for k, value in enumerate(mooring_lat):
        if (mooring_lat[k] != 0.0) and (mooring_lon[k] != 0.0):
            geojson_point_coords = geojson_point_coords + ('{{"type": "Feature","geometry": {{"type": "Point","coordinates": [{1},{0}]}}, "properties": {{"MooringID":"{2}" }}}}').format(mooring_lat[k],mooring_lon[k],mooringid[k])
        
            if (k+1 != len(mooring_lat)):
                geojson_point_coords = geojson_point_coords + ', '

    geojson_tail = (
        ']\n'
        '}\n'
        )
    
    print geojson_header + geojson_point_coords + geojson_tail 
    
if args.google_earth:

    point_coords = ''
    for k, value in enumerate(mooring_lat):
        if (mooring_lat[k] != 0.0) and (mooring_lon[k] != 0.0):
            point_coords = point_coords + ('new google.maps.LatLng({0},{1})').format(mooring_lat[k],mooring_lon[k])

            if (k+1 != len(mooring_lat)):
                point_coords = point_coords + ',\n'
    print point_coords