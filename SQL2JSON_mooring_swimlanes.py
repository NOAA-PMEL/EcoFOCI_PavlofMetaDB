#!/usr/bin/env

"""
 SQL2JSON_mooring_swimlanes.py
 
 Purpose:
 --------

 Build an html file that utilizes the swimlane D3.js graphic.  

 Its a dynamic webpage that allows one to visualize the deployment duration of each FOCI mooring in the database

"""

# System Stack
import datetime
import pymysql
import argparse

#User Stack
from io_utils.EcoFOCI_db_io import EcoFOCI_db_datastatus

__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2014, 04, 04)
__modified__ = datetime.datetime(2016, 10, 17)
__version__  = "0.2.0"
__status__   = "Development"
__keywords__ = 'CTD', 'MetaInformation', 'Cruise', 'MySQL', 'website', 'PMEL', 'JSON'


"""------------------------------------------------------------------------------------"""
parser = argparse.ArgumentParser(description='MySQL database --> json wrapped swimlanes file')
parser.add_argument('-mid','--moorings', 
	action="store_true", 
	help='processing FOCI mooring deployment/recovery data')
parser.add_argument('-inst', '--instruments', 
	action="store_true", 
	help='processing all historic FOCI instrument deployment/recovery data')
parser.add_argument('-inst_a', '--instruments_active', 
	action="store_true", 
	help='processing only active FOCI instrument deployment/recovery data')

# deployment data
EcoFOCI_db = EcoFOCI_db_datastatus()
config_file = 'EcoFOCI_config/db_config/db_config_mooring.pyini'
(db,cursor) = EcoFOCI_db.connect_to_DB(db_config_file=config_file)
MooringDeploymentData = EcoFOCI_db.read_mooring_summary(table='mooringdeploymentlogs')
EcoFOCI_db.close()

# recovery data
EcoFOCI_db = EcoFOCI_db_datastatus()
config_file = 'EcoFOCI_config/db_config/db_config_mooring.pyini'
(db,cursor) = EcoFOCI_db.connect_to_DB(db_config_file=config_file)
MooringDeploymentData = EcoFOCI_db.read_mooring_summary(table='mooringrecoverylogs')
EcoFOCI_db.close()