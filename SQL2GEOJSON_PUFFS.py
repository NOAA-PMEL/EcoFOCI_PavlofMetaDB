#!/usr/bin/env python

"""
SQL2GEOJSON_PUFFS.py
 
export all ctd cast locations to geojson format for plotting


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
__created__  = datetime.datetime(2015, 5, 28)
__modified__ = datetime.datetime(2015, 5, 28)
__version__  = "0.1.0"
__status__   = "Development"
__keywords__ = 'moorings','csv','google maps', 'heatmap', 'geojson'



"""------------------------------- MAIN ----------------------------------------"""

parser = argparse.ArgumentParser(description='Cruise Database -> GEOJSON')
parser.add_argument('--geojson', action='store_true', help='create geojson file')

args = parser.parse_args()

#get information from local config file - a json formatted file
config_file = 'EcoFOCI_config/db_config/db_config_drifters.yaml'

EcoFOCI_db = EcoFOCI_PUFF_db_datastatus()
(db,cursor) = EcoFOCI_db.connect_to_DB(db_config_file=config_file,ftype='yaml')

data_mooring = EcoFOCI_db.read_floats(table='popupfloats_deployed')

if args.geojson:
    ### "Generating .geojson"
    geojson_header = (
        '{\n'
        '"type": "FeatureCollection",\n'
        '"features": [\n'
        '{\n'
        '"type": "Feature",\n'
        '"geometry": {\n'
        '"type": "MultiPoint",\n'
        '"coordinates": [ '
        )
    geojson_point_coords = ''

    for a_ind in sorted(data_puffs.keys()):
        point_coords = point_coords + ('new google.maps.LatLng({0},{1})').format(data_puffs[a_ind]['DEPLOY_LAT'],data_puffs[a_ind]['DEPLOY_LON'])

        if (a_ind != sorted(data_puffs.keys())[-1]):
            geojson_point_coords = geojson_point_coords + ', '

    geojson_tail = (
        ']\n'
        '},\n'
        '"properties": {\n'
        '"prop0": "value0"\n'
        '}\n'
        '}\n'
        ']\n'
        '}\n'
        )
    
    print(geojson_header+geojson_point_coords+geojson_tail) 
    
