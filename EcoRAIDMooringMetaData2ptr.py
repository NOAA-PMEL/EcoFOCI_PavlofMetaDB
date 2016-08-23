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
import pymysql
import argparse

#User Stack
import io_utils.ConfigParserLocal as ConfigParserLocal

__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2016, 8, 20)
__modified__ = datetime.datetime(2016, 8, 20)
__version__  = "0.1.0"
__status__   = "Development"


