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
from io_utils.EcoFOCI_db_io import EcoFOCI_PUFF_db_datastatus


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

data_puffs = EcoFOCI_db.read_floats(table='popupfloats_deployed')

if args.geojson:
    ### "Generating .geojson"
    geojson_header = (
        '{"type": "FeatureCollection","features": ['
        )
    geojson_point_coords = ''

    for a_ind in sorted(data_puffs.keys()):
        geojson_point_coords = geojson_point_coords + ('''
        {{"type": "Feature","geometry": 
        {{"type": "Point","coordinates": [{1},{0}]}}, 
        "properties": {{"ENG_SN":"{2}", "IMEI_SN":"{3}","GEN":"{4}", "DEPLOY_CRUISE":"{5}",
        "SITE":"{6}", "DEPLOY_DEPTH_meters":"{7}", "DEPLOY_ DATETIMEUTC":"{8}", "UNIT_START_DATETIMEUTC":"{9}",
        "RELEASE_DATETIMEUTC":"{10}", "UNIT_START_DATETIMEUTC":"{11}"}}}}''').format(data_puffs[a_ind]['DEPLOY_LAT'],
        data_puffs[a_ind]['DEPLOY_LON'],data_puffs[a_ind]['ENG_SN'],data_puffs[a_ind]['IMEI_SN'],
        data_puffs[a_ind]['GEN'],data_puffs[a_ind]['DEPLOY_CRUISE'],data_puffs[a_ind]['SITE'],
        data_puffs[a_ind]['DEPLOY_DEPTH_meters'],data_puffs[a_ind]['DEPLOY_ DATETIMEUTC'],data_puffs[a_ind]['UNIT_START_DATETIMEUTC'],
        data_puffs[a_ind]['RELEASE_DATETIMEUTC'],data_puffs[a_ind]['DEPLOY_FISCAL_YEAR'])

        if (a_ind != sorted(data_puffs.keys())[-1]):
            geojson_point_coords = geojson_point_coords + ', '

    geojson_tail = (
        ']\n'
        '}\n'
        )
        
    print(geojson_header+geojson_point_coords+geojson_tail) 
    
