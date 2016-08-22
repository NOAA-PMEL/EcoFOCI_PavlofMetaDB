#!/usr/bin/env

"""
 EcoRAIDMooringMetaData2SQL.py
 
 Populates Database with status of mooring processing from ecoraid archive

 Using Anaconda packaged Python 
"""

import os
import sys
import datetime
import pymysql
import argparse

#Science Stack
from netCDF4 import Dataset #netcdf usage
import numpy as np

#User Stack
import utilities.ConfigParserLocal as ConfigParserLocal

__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2014, 8, 8)
__modified__ = datetime.datetime(2014, 8, 8)
__version__  = "0.1.0"
__status__   = "Development"

"""------------------------General   Modules-------------------------------------------"""

def walk_dir(search_dir, ncEnding='.nc'):
    """Walk through given directory and return a list of all valid paths as well as a list
    of filenames only.
        nc_ending is a variable that holds the pattern for the end of the .nc files..
    """
    allroot = []
    allfile = []
    for root, dirs, files in os.walk(search_dir):
        for file in files:
            if file.endswith(ncEnding):
                allroot.append(os.path.join(root, file))
                allfile.append(file) 
    return (allroot, allfile)
    


"""--------------------------------SQL Init----------------------------------------"""

def connect_to_DB(host, user, password, database, port):
    # Open database connection
    try:
        db = pymysql.connect(host, user, password, database, port)
    except:
        print "db error"
        
    # prepare a cursor object using cursor() method
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return(db,cursor)
    

def add_to_DB(db,cursor,table,data_dic):
    """
    General format:

    """
    # Prepare SQL query to INSERT a record into the database.
    sql = ("INSERT INTO `{!s}`(year, recordtype, "
            "mooringid, instrumenttype, isinitialarchive, isfinaldata, filenameinitial, "
            "filenamefinal, instdepth) "
            "VALUES ('{!s}', '{!s}', '{!s}', '{!s}', '{!s}', '{!s}', '{!s}', '{!s}', '{!s}'"
            ")" .format(table,data_dic['year'],data_dic['recordtype'],data_dic['mooringid'],\
            data_dic['instrumenttype'],data_dic['isinitialarchive'],data_dic['isfinaldata'],\
            data_dic['filenameinitial'], data_dic['filenamefinal'], data_dic['instdepth']))
    #print sql
    try:
       # Execute the SQL command
       cursor.execute(sql)
       print "insert record success"
       # Commit your changes in the database
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()

def update_DB(db,cursor,table,data_dic):
    sql = ("UPDATE `{!s}` SET `filenamefinal`='{!s}', `isfinaldata`='{!s}' "
    "WHERE `mooringid` = '{!s}' AND instdepth = '{!s}' AND instrumenttype = '{!s}' "
    "AND isspecialarchive = 'n'".format(\
    table,data_dic['filenamefinal'],data_dic['isfinaldata'], data_dic['mooringid'], \
    data_dic['instdepth'], data_dic['instrumenttype']))
    #print sql
    try:
       # Execute the SQL command
       cursor.execute(sql)
       print "update record success"
       # Commit your changes in the database
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()
       
def check_db_entry_exists(db, cursor, table, data_dic):
    sql = ("SELECT COUNT(1) FROM `%s` WHERE mooringid = '%s' "
    "AND instdepth = '%s' AND instrumenttype = '%s' "
    "AND isspecialarchive = 'n'" % \
             (table, data_dic['mooringid'], data_dic['instdepth'], data_dic['instrumenttype']))

    cursor.execute(sql)
    if cursor.fetchone()['COUNT(1)']:
        return (True)
    else:
        return (False)

"""------------------------------------------------------------------------------------"""
parser = argparse.ArgumentParser(description='.nc -> MySQL database')
parser.add_argument('nc_path', metavar='nc_path', type=str,help='root path to data to be ingested')
parser.add_argument('nc_path_year', metavar='nc_path_year', type=str,help='root path to data to be ingested')
parser.add_argument('datatype', metavar='datatype', type=str,help="'Moorings','CTDCasts','AlongTrack'")

args = parser.parse_args()

if args.datatype not in ['Moorings','CTDCasts','AlongTrack']:
    raise RuntimeError("Choose from 'Moorings','CTDCasts','AlongTrack'")

insttype = ['sc','s37','s39','s56','mt','wpak','an7','an9','an11','ecf','adcp','wcp','lrcp','isus','suna','']

#get information from local config file - a json formatted file
db_config = ConfigParserLocal.get_config('../db_connection_config_files/db_config_datastatus.pyini')

### Get list of NCFiles
nc_path = args.nc_path + args.nc_path_year + '/'
nc_dir, ncfileonly = walk_dir(nc_path, ncEnding='.nc')

if args.datatype.lower() == 'moorings':
    ### connect to DB
    (db,cursor) = connect_to_DB(db_config['host'], db_config['user'], db_config['password'], db_config['database'], db_config['port'])

    #build and look for initial data first
    for i, nc_file in enumerate(nc_dir): 
        data_dic = {}
        parsed_file = nc_file.split('/')
        if args.datatype in parsed_file:

            countind = parsed_file.index(args.datatype)
            data_dic['year'] = args.nc_path_year
            data_dic['recordtype'] = args.datatype
            data_dic['mooringid'] = parsed_file[countind + 1]
            data_dic['isinitialarchive'] = 'n'
            data_dic['filenamefinal'] = ''        
            data_dic['isfinaldata'] = 'n'

            if parsed_file[countind + 2] == 'initial_archive':
                data_dic['isinitialarchive'] = 'y'
                try:
                    data_dic['instrumenttype'] = parsed_file[countind + 3].split('_')[1]
                except:
                    print "Something is odd - {0}: skipping".format(parsed_file)
                    continue
                try:
                    data_dic['instdepth'] = parsed_file[countind + 3].split('_')[2].split('m')[0]
                except:
                    pass
                if 'mt' in data_dic['instrumenttype']:
                    data_dic['instrumenttype'] = 'mt'
                elif 'wpak' in data_dic['instrumenttype']:
                    data_dic['instrumenttype'] = 'wpak'
                    data_dic['instdepth'] = '0000'
                elif 'ISUS' in data_dic['instrumenttype']:
                    data_dic['instrumenttype'] = 'isus'
                elif 'wcp' in data_dic['instrumenttype']:
                    data_dic['instdepth'] = '0000'
                elif 'lrcp' in data_dic['instrumenttype']:
                    data_dic['instdepth'] = '0000'
                if not data_dic['instrumenttype'] in insttype:
                    print "{0} not an instumenttype listed in database".format(data_dic['instrumenttype'])
                    continue
                data_dic['filenameinitial'] = parsed_file[-1]
            
        if data_dic.has_key('instrumenttype'):
            if not check_db_entry_exists(db,cursor,'ecoraid_filemetainfo',data_dic):
                print "Adding initial data only"
                add_to_DB(db,cursor,'ecoraid_filemetainfo',data_dic)
            else:
                print "Record {0}:{1} exists".format(data_dic['mooringid'], data_dic['instrumenttype'])
            
    #build and look for final data
    for i, nc_file in enumerate(nc_dir): 
        data_dic = {}
        parsed_file = nc_file.split('/')
        if args.datatype in parsed_file:

            countind = parsed_file.index(args.datatype)
            data_dic['year'] = args.nc_path_year
            data_dic['recordtype'] = args.datatype
            data_dic['mooringid'] = parsed_file[countind + 1]
            data_dic['isfinaldata'] = 'n'

            if parsed_file[countind + 2] == 'final_data':
                data_dic['isfinaldata'] = 'y'
                try:
                    data_dic['instrumenttype'] = parsed_file[countind + 3].split('_')[1]
                except:
                    print "Something is odd - {0}: skipping".format(parsed_file)
                    continue
                try:
                    data_dic['instdepth'] = parsed_file[countind + 3].split('_')[2].split('m')[0]
                except:
                    pass
                if 'mt' in data_dic['instrumenttype']:
                    data_dic['instrumenttype'] = 'mt'
                elif 'wpak' in data_dic['instrumenttype']:
                    data_dic['instrumenttype'] = 'wpak'
                    data_dic['instdepth'] = '0000'
                elif 'ISUS' in data_dic['instrumenttype']:
                    data_dic['instrumenttype'] = 'isus'
                elif 'wcp' in data_dic['instrumenttype']:
                    data_dic['instdepth'] = '0000'
                elif 'lrcp' in data_dic['instrumenttype']:
                    data_dic['instdepth'] = '0000'
                if not data_dic['instrumenttype'] in insttype:
                    print "{0} not an instumenttype listed in database".format(data_dic['instrumenttype'])
                    continue
                data_dic['filenamefinal'] = parsed_file[-1]

        if data_dic.has_key('instrumenttype'):
            if not check_db_entry_exists(db,cursor,'ecoraid_filemetainfo',data_dic):
                print "Adding final data only"
                data_dic['isinitialarchive'] = 'n'
                data_dic['filenameinitial'] = ''
                add_to_DB(db,cursor,'ecoraid_filemetainfo',data_dic)
            else:
                print "Updating {0}:{1} final data record".format(data_dic['mooringid'], data_dic['instrumenttype'])
                update_DB(db,cursor,'ecoraid_filemetainfo',data_dic)
    db.close()

