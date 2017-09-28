#!/usr/bin/env

"""
 SQL2JSON_mooring_timeline.py
 
 build a JSON driven html file for Mooring timelines

 Using Anaconda packaged Python 
"""

# System Stack
import datetime
import pymysql
import argparse

#User Stack
import utilities.ConfigParserLocal as ConfigParserLocal

__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2014, 04, 04)
__modified__ = datetime.datetime(2014, 04, 04)
__version__  = "0.1.0"
__status__   = "Development"
__keywords__ = 'CTD', 'MetaInformation', 'Cruise', 'MySQL', 'website', 'PMEL', 'JSON'

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
    
def read_mooring(db, cursor, table):
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
            result_dic[row['MooringID']] ={keys: row[keys] for val, keys in enumerate(row.keys())} 
        return (result_dic)
    except:
        print "Error: unable to fecth data"

def latlon_convert(lat, lon, format='ddd mm.ss'):
    if format == 'ddd mm.ss':
        latdd = float(lat.split()[0]) + float(lat.split()[1])/60.0
        londd = -1.0*(float(lon.split()[0]) + float(lon.split()[1])/60.0)

    return (latdd,londd)
"""----------------------------------Main----------------------------------------------"""

parser = argparse.ArgumentParser(description='Mooring DB -> CSV -- Summary Files')
parser.add_argument('--timeline', action='store_true', help='list of moorings without yearid')
args = parser.parse_args()

#get information from local config file - a json formatted file
db_config = ConfigParserLocal.get_config('../db_connection_config_files/db_config_mooring.pyini')

tablelist=['mooringdeploymentlogs','mooringrecoverylogs']

    
(db,cursor) = connect_to_DB(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
Mooring_Meta_dep = read_mooring(db, cursor, tablelist[0])
Mooring_Meta_rec = read_mooring(db, cursor, tablelist[1])
close_DB(db)
 
if not args.timeline:
    print "MooringID, Lat, Lon, DeployDate, RecoveryDate"
    for mooring in sorted(Mooring_Meta_dep.keys()):
        if mooring == Mooring_Meta_rec[mooring]['MooringID']:
            try:
                lat,lon = latlon_convert(Mooring_Meta_dep[mooring]['Latitude'], Mooring_Meta_dep[mooring]['Longitude'])
                print "{0}, {1}, {2}, {3}, {4}".format(mooring,  lat, lon, \
                      Mooring_Meta_dep[mooring]['DeploymentDateTimeGMT'], Mooring_Meta_rec[mooring]['RecoveryDateTimeGMT'])
            except:
                #invalid locations
                continue
            
else:
    mooring_stas = sorted(list(set([x[2:] for x in sorted(Mooring_Meta_dep.keys())])))
    print "FullMooringID, MooringID, MooringSite, Lat, Lon, DeployDate, RecoveryDate, DepLengthDays"
    for moorings in mooring_stas:
        for mooring in sorted(Mooring_Meta_dep.keys()):
            if moorings == Mooring_Meta_rec[mooring]['MooringID'][2:]:
                try:
                    lat,lon = latlon_convert(Mooring_Meta_dep[mooring]['Latitude'], Mooring_Meta_dep[mooring]['Longitude'])
                    try:
                        DepLength = (Mooring_Meta_rec[mooring]['RecoveryDateTimeGMT']-Mooring_Meta_dep[mooring]['DeploymentDateTimeGMT'])
                    except:
                        DepLength = datetime.timedelta(365)
                    moor_num = moorings.split('-')[0][:2] + '-' + moorings.split('-')[-1][:-1]
                    print "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(Mooring_Meta_dep[mooring]['MooringID'], moorings, moor_num,  lat, lon, \
                          Mooring_Meta_dep[mooring]['DeploymentDateTimeGMT'], Mooring_Meta_rec[mooring]['RecoveryDateTimeGMT'], DepLength.days)
                except KeyError:
                    #invalid locations
                    print "ha!!!"
                    continue
                except IndexError:
                    continue
                except ValueError:
                    continue
                
