#!/usr/bin/env python

"""
SQL2GEOJSON_Moorings.py
 
export all ctd cast locations to geojson format for plotting


"""

#System Stack
import datetime
import argparse
import pymysql
import sys

#Science Stack
import numpy as np

#User Stack
import utilities.ConfigParserLocal as ConfigParserLocal


__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2015, 05, 28)
__modified__ = datetime.datetime(2015, 05, 28)
__version__  = "0.1.0"
__status__   = "Development"
__keywords__ = 'moorings','csv','google maps', 'heatmap', 'geojson'

"""--------------------------------SQL Init----------------------------------------"""

def connect_to_DB(host, user, password, database):
    # Open database connection
    try:
        db = pymysql.connect(host, user, password, database)
    except:
        print "db error"
        
    # prepare a cursor object using cursor() method
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return(db,cursor)


def close_DB(db):
    # disconnect from server
    db.close()
    
def read_casts(db, cursor, table):
    sql = "SELECT * from `%s`" % (table)
    #print sql
    
    result_dic = {}
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Get column names
        rowid = {}
        counter = 0
        for i in cursor.description:
            rowid[i[0]] = counter
            counter = counter +1 
        #print rowid
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            result_dic[row['id']] ={keys: row[keys] for val, keys in enumerate(row.keys())} 
        return (result_dic)
    except:
        print "Error: unable to fecth data"


"""------------------------------- MAIN ----------------------------------------"""

parser = argparse.ArgumentParser(description='Cruise Database -> GEOJSON')
parser.add_argument('--geojson', action='store_true', help='create geojson file')
parser.add_argument('--google_earth', action='store_true', help='create google earth file')

args = parser.parse_args()

#get information from local config file - a json formatted file
db_config = ConfigParserLocal.get_config('../db_connection_config_files/db_config_cruises.pyini')

(db,cursor) = connect_to_DB(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
data_mooring = read_casts(db, cursor, 'cruisecastlogs')

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

    for a_ind in sorted(data_mooring.keys()):
        if not (data_mooring[a_ind]['LatitudeDeg'] == '-99') or (data_mooring[a_ind]['LongitudeDeg'] == '-999'):
            point_coords = point_coords + ('new google.maps.LatLng({0},{1})').format(data_mooring[a_ind]['LatitudeDeg']+data_mooring[a_ind]['LatitudeMin']/60.,-1.0*(data_mooring[a_ind]['LongitudeDeg']+data_mooring[a_ind]['LongitudeMin']/60.))

            if (a_ind != sorted(data_mooring.keys())[-1]):
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
    
    print geojson_header + geojson_point_coords + geojson_tail 
    
if args.google_earth:

    point_coords = ''
    for a_ind in sorted(data_mooring.keys()):
        if not (data_mooring[a_ind]['LatitudeDeg'] == '-99') or (data_mooring[a_ind]['LongitudeDeg'] == '-999'):
            point_coords = point_coords + ('new google.maps.LatLng({0},{1})').format(data_mooring[a_ind]['LatitudeDeg']+data_mooring[a_ind]['LatitudeMin']/60.,-1.0*(data_mooring[a_ind]['LongitudeDeg']+data_mooring[a_ind]['LongitudeMin']/60.))

            if (a_ind != sorted(data_mooring.keys())[-1]):
                point_coords = point_coords + ',\n'
    print point_coords