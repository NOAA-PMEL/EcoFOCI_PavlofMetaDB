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
(db,cursor) = EcoFOCI_db.connect_to_DB()