#!/usr/bin/env python

"""
 DBMooringSummary.py
 
 Input: MooringID (eg. 14bsm2a or 14BSM-2A)
 Output: text file with...
    mooring charactersistcs
    instruments deployed, depths, serial numbers

History:
=======

2021-3-25: add yaml output for moorings
2020-12-2: python3 only 

Compatibility:
==============
python >=3.6 - Tested
python 2.7 - **no longer supported


"""

import sys

# must be python 3.6 or greater
try:
    assert sys.version_info > (3, 6)
except AssertionError:
    sys.exit("Must be running python 3")

import argparse
import collections
import datetime

import yaml

from io_utils import ConfigParserLocal
from io_utils.EcoFOCI_db_io import EcoFOCI_db_datastatus

__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2014, 1, 13)
__modified__ = datetime.datetime(2021, 3, 24)
__version__  = "0.3.0"
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
parser.add_argument('MooringID', metavar='MooringID', type=str, help='MooringID eg 13BSM-2A')               
parser.add_argument('-db', '--db_ini', type=str, help='path to db .yaml file')               
parser.add_argument('-wf', '--wiki_format', action="store_true", help='format for wiki')               
parser.add_argument('-yaml', '--yaml_format', action="store_true", help='format for yaml files')               

args = parser.parse_args()
    
#get information from local config file - a json formatted file
if args.db_ini:
    config_file = args.db_ini
else:
    config_file = 'EcoFOCI_config/db_config/db_config_mooring.yaml'


EcoFOCI_db = EcoFOCI_db_datastatus()
(db,cursor) = EcoFOCI_db.connect_to_DB(db_config_file=config_file)

#get db meta information for mooring
table = 'mooringdeployedinstruments'
Mooring_Meta_inst = EcoFOCI_db.read_mooring_inst(table=table, mooringid=args.MooringID, verbose=True)
table = 'mooringdeploymentlogs'
Mooring_Meta_sum = EcoFOCI_db.read_mooring_summary(table=table, mooringid=args.MooringID, verbose=True)
table = 'mooringrecoverylogs'
Mooring_recovery_sum = EcoFOCI_db.read_mooring_summary(table=table, mooringid=args.MooringID)
table = 'mooringdeploymentnotes'
Mooring_Meta_notes = EcoFOCI_db.read_mooring_summary(table=table, mooringid=args.MooringID)

EcoFOCI_db.close()

try:
    Mooring_Meta_sum[args.MooringID]
except:
    print("No known mooring {0}.  Check syntax and case (e.g. 14BSM-2A)".format(args.MooringID))
    sys.exit()
    
if args.wiki_format:
    print(("Cruise:\t\t[[ {0}|{0} ]]\n").format(Mooring_Meta_sum[args.MooringID]['CruiseNumber']))
    print(("Latitude:\t{0}\n").format(Mooring_Meta_sum[args.MooringID]['Latitude']))
    print(("Longitude:\t{0}\n").format(Mooring_Meta_sum[args.MooringID]['Longitude']))
    print(("DeploymentDateTimeGMT:\t{0}\n").format(Mooring_Meta_sum[args.MooringID]['DeploymentDateTimeGMT']))
    print(("RecoveryDateTimeGMT:\t{0}\n").format(Mooring_recovery_sum[args.MooringID]['RecoveryDateTimeGMT']))

    print(("Comments:\t{0}\n").format(Mooring_Meta_notes[args.MooringID]['Comments']))

    print("""

    ==INSTRUMENT SUMMARY==

    {|class="wikitable sortable"
    !Instrument!!Serial Number!!Depth!!Data Status!!Notes""")

    for instrument in sorted(Mooring_Meta_inst.keys()):
        ### specific text processing for long named instuments to map to a clean format
        if ('release' in Mooring_Meta_inst[instrument]['InstType']):
            continue
        if ('FLSB' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'ecoFLSB'        
        if ('BBFL' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'ecoTrip'        
        if ('Weatherpak' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'wpak'        
        if ('RDI 300 KHz ADCP' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'adcp'        
        if ('float' in Mooring_Meta_inst[instrument]['InstType'].lower()):
            continue        
        if ('McClain' in Mooring_Meta_inst[instrument]['InstType']):
            continue        

        print (("|-\n|{0}||{1}||{2}||{3}||{4}").format(
        Mooring_Meta_inst[instrument]['InstType'],Mooring_Meta_inst[instrument]['SerialNo'], Mooring_Meta_inst[instrument]['Depth'],
        Mooring_Meta_inst[instrument]['DataStatus'], Mooring_Meta_inst[instrument]['PostDeploymentNotes']))

    print("""|-\n|}
    
    ==Data Processing Description and Notes==

    """)

elif args.yaml_format:
    data_dic = {'MooringID':None, 'Deployment':None, 'Recovery':None, 'Notes':None, 'Instrumentation':None}
    data_dic['MooringID'] = args.MooringID

    try:
        data_dic['Deployment'] = {'DeploymentCruise':Mooring_Meta_sum[args.MooringID]['CruiseNumber'],
                        'DeploymentLatitude':Mooring_Meta_sum[args.MooringID]['Latitude'],
                        'DeploymentLongitude':Mooring_Meta_sum[args.MooringID]['Longitude'],
                        'DeploymentDateTimeGMT':Mooring_Meta_sum[args.MooringID]['DeploymentDateTimeGMT'],
                        'DeploymentDepth':Mooring_Meta_sum[args.MooringID]['DeploymentDepth']}
    except:
        print(f'No Deployment Data for {args.MooringID}')
    try:
        data_dic['Recovery'] = {'RecoveryCruise':Mooring_recovery_sum[args.MooringID]['CruiseNumber'],
                     'RecoveryLatitude':Mooring_recovery_sum[args.MooringID]['Latitude'],
                     'RecoveryLongitude':Mooring_recovery_sum[args.MooringID]['Longitude'],
                     'RecoveryDateTimeGMT':Mooring_recovery_sum[args.MooringID]['RecoveryDateTimeGMT'],
                     'RecoveryDepth':Mooring_recovery_sum[args.MooringID]['DeploymentDepth']}
    except:
        print(f'No Recovery Data for {args.MooringID}')


    #Predepolyment Information
    try:
        data_dic['Notes'] = Mooring_Meta_notes[args.MooringID]['Comments']
    except:
        print(f'No Notes for {args.MooringID}')

    #build a dictionary of dictionaries for instrumentation
    InstrumentDic = {}

    try:
        for instrument in sorted(Mooring_Meta_inst.keys()):
            InstrumentDic[Mooring_Meta_inst[instrument]['InstID']] = {'InstType':Mooring_Meta_inst[instrument]['InstType'],
                                'SerialNo':Mooring_Meta_inst[instrument]['SerialNo'],
                                'DesignedDepth':Mooring_Meta_inst[instrument]['Depth'],
                                'ActualDepth':Mooring_Meta_inst[instrument]['ActualDepth'],
                                'PreDeploymentNotes':Mooring_Meta_inst[instrument]['PreDeploymentNotes'],
                                'PostDeploymentNotes':Mooring_Meta_inst[instrument]['PostDeploymentNotes'],
                                'Deployed':Mooring_Meta_inst[instrument]['Deployed'],
                                'Recovered':Mooring_Meta_inst[instrument]['Recovered']}
        
        data_dic['Instrumentation'] = InstrumentDic
    except:
        print(f'Instrument listing failed for {args.MooringID}')
        
    ConfigParserLocal.write_config(args.MooringID+'.yaml', data_dic)

else:
    print("{0} README".format(args.MooringID))
    print(" \n")
    print(("Cruise:\t\t{0}").format(Mooring_Meta_sum[args.MooringID]['CruiseNumber']))
    print(("Latitude:\t{0}").format(Mooring_Meta_sum[args.MooringID]['Latitude']))
    print(("Longitude:\t{0}").format(Mooring_Meta_sum[args.MooringID]['Longitude']))
    print(("Deployment Depth:\t{0}m\n").format(Mooring_Meta_sum[args.MooringID]['DeploymentDepth']))
    print(("DeploymentDateTimeGMT:\t{0}\n").format(Mooring_Meta_sum[args.MooringID]['DeploymentDateTimeGMT']))
    print(("RecoveryDateTimeGMT:\t{0}").format(Mooring_recovery_sum[args.MooringID]['RecoveryDateTimeGMT']))

    print("""

Processed by: 

    """)
    print(("Comments:\t{0}\n").format(Mooring_Meta_notes[args.MooringID]['Comments']))

    print("""
DATA SUMMARY
============

Instrument\tSerial \t\tDepth\t\tDepth\t\t   Data   \t\tNotes
          \tNumber \t\t(est)\t\t(act)\t\t   Status \t\t 
----------\t-------\t\t-----\t\t-----\t\t----------\t\t------
    """)
            
    for instrument in sorted(Mooring_Meta_inst.keys()):
        ### specific text processing for long named instuments to map to a clean format
        if ('release' in Mooring_Meta_inst[instrument]['InstType']):
            continue
        if ('FLSB' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'ecoFLSB'        
        if ('BBFL' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'ecoTrip'        
        if ('Weatherpak' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'wpak'        
        if ('RDI 300 KHz ADCP' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'adcp'        
        if ('float' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'float'        
        if ('FLOAT' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'float'        
        if ('Float' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'float'        
        if ('McClain' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'float'        
        if ('Flotation' in Mooring_Meta_inst[instrument]['InstType']):
            Mooring_Meta_inst[instrument]['InstType'] = 'float' 

        print (("{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{5}").format(
        Mooring_Meta_inst[instrument]['InstType'],Mooring_Meta_inst[instrument]['SerialNo'], Mooring_Meta_inst[instrument]['Depth'],
        Mooring_Meta_inst[instrument]['ActualDepth'],Mooring_Meta_inst[instrument]['DataStatus'], Mooring_Meta_inst[instrument]['PostDeploymentNotes']))

    print("""

General Notes:
==============



CTD_Cal_Casts:
--------------
(***) - most relevant

    """)
