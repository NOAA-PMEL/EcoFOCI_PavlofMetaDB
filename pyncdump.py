#!/usr/bin/env python

"""
pyncdump.py

 Purpose:
 -----

 Python alternative to ncdump for metainfo

 Usage:
 ------
 pyncdump -i {filename}

 
 History:
 ========
 2020-03-26: EPIC time conversion modified to support python3, format statements modified for python3
 2016-11-11: SBELL - move routine from general_utilities and unify class/subroutines with
 other EcoFOCI utilities


 Compatibility:
 ==============
 python >=3.7 ** tested
 python 2.7 ** tested but no longer developed for
"""

# System Stack
import datetime
import os
import argparse

# Science Stack
from netCDF4 import Dataset
import numpy as np

# user stack
from io_utils.EcoFOCI_netCDF_read import EcoFOCI_netCDF
from calc.EPIC2Datetime import EPIC2Datetime

import warnings

warnings.filterwarnings("ignore")

__author__ = "Shaun Bell"
__email__ = "shaun.bell@noaa.gov"
__created__ = datetime.datetime(2016, 11, 12)
__modified__ = datetime.datetime(2016, 11, 12)
__version__ = "0.2.0"
__status__ = "Development"
__keywords__ = "netCDF", "meta", "header"


"""---------------------------------- Main --------------------------------------------"""
try:
    os.system("clear")
except:
    pass

parser = argparse.ArgumentParser(description="Summary of input .nc file.")
parser.add_argument("infile", metavar="infile", type=str, help="input file path")


args = parser.parse_args()

os.system("clear")

inputpath = args.infile

###nc readin/out
df = EcoFOCI_netCDF(args.infile)
global_atts = df.get_global_atts()
vars_dic = df.get_vars()
ncdata = df.ncreadfile_dic()

# convert epic time
# time2 wont exist if it isnt epic keyed time
if "time2" in vars_dic.keys():
    ncdata["datetime"] = EPIC2Datetime(ncdata["time"], ncdata["time2"])

"""----------"""
###screen output

if len(ncdata["time"]) > 1:
    print("\n\n\n\n\n\n")
    print("Filename - {0} \n").format(inputpath)
    for var in vars_dic.keys():
        v_atts = df.get_vars_attributes(var)
        try:
            ncdata[var][ncdata[var] >= 1e34] = np.nan
        except:
            pass
        try:
            print(
                "\tVariable: {1}\n\t\t Epic Key: {0:_<10} :\t min={2:>15.3f} \t max={3:>15.3f} \t mean={4:>15.3f} \t median={5:>15.3f}".format(
                    var,
                    v_atts.long_name,
                    np.nanmin(ncdata[var]),
                    np.nanmax(ncdata[var]),
                    np.nanmean(ncdata[var]),
                    np.nanmedian(ncdata[var]),
                )
            )
        except:
            print(
                "\tVariable: {1}\n\t\t Epic Key: {0:_<10} :\t min={2:>15.3f} \t max={3:>15.3f} \t mean={4:>15.3f} \t median={5:>15.3f}".format(
                    var,
                    "",
                    np.nanmin(ncdata[var]),
                    np.nanmax(ncdata[var]),
                    np.nanmean(ncdata[var]),
                    np.nanmedian(ncdata[var]),
                )
            )
    print("\n")

    ### EPIC standard time conversion - assume time2 dimension exists
    if "time2" in vars_dic.keys():
        print("            EPIC time conversion:\n")
        print("\t Start Time: {:%Y-%m-%d %H:%M:%S}".format(np.min(ncdata["datetime"])))
        print("\t End Time: {:%Y-%m-%d %H:%M:%S}".format(np.max(ncdata["datetime"])))
        print(
            "\t DeltaT based on first two points: {0} seconds".format(
                (ncdata["datetime"][1] - ncdata["datetime"][0]).seconds
            )
        )
        print(
            "\t DeltaT based on last two points: {0} seconds".format(
                (ncdata["datetime"][-1] - ncdata["datetime"][-2]).seconds
            )
        )

    print("\nGlobal Attributes:\n")
    for var in global_atts.keys():
        try:
            print("\t {0}: {1}".format(var, global_atts[var]))
        except UnicodeEncodeError:
            print("\t {0}: {1}".format(var, "***Unrecognized ASCII characters***"))
    print("\n")
    print("Variables in file: {list}".format(list=",".join(vars_dic.keys())))
    print("\n\n\n")
else:
    print("\n\n\n\n\n\n")
    print("Filename - {0} \n".format(inputpath))
    for var in vars_dic.keys():
        v_atts = df.get_vars_attributes(var)
        try:
            ncdata[var][ncdata[var] >= 1e34] = np.nan
        except:
            pass
        try:
            print(
                "\tVariable: {1}\n\t\t Epic Key: {0:_<10} :\t min={2:>15.3f} \t max={3:>15.3f} \t mean={4:>15.3f} \t median={5:>15.3f}".format(
                    var,
                    v_atts.long_name,
                    np.nanmin(ncdata[var]),
                    np.nanmax(ncdata[var]),
                    np.nanmean(ncdata[var]),
                    np.nanmedian(ncdata[var]),
                )
            )
        except:
            print(
                "\tVariable: {1}\n\t\t Epic Key: {0:_<10} :\t min={2:>15.3f} \t max={3:>15.3f} \t mean={4:>15.3f} \t median={5:>15.3f}".format(
                    var,
                    "",
                    np.nanmin(ncdata[var]),
                    np.nanmax(ncdata[var]),
                    np.nanmean(ncdata[var]),
                    np.nanmedian(ncdata[var]),
                )
            )
    print("\n")

    ### EPIC standard time conversion - assume time2 dimension exists
    if "time2" in vars_dic.keys():
        print("            EPIC time conversion:\n")
        print("\t Cast Time: {:%Y-%m-%d %H:%M:%S}".format(np.min(ncdata["datetime"])))
        try:
            print(
                "\t Depth Interval: {0} dBar".format(
                    (ncdata["depth"][1] - ncdata["depth"][0])
                )
            )
        except:
            print(
                "\t Depth Interval: {0} dBar".format(
                    (ncdata["dep"][1] - ncdata["dep"][0])
                )
            )

    print("\nGlobal Attributes:\n")
    for var in global_atts.keys():
        try:
            print("\t {0}: {1}".format(var, global_atts[var]))
        except UnicodeEncodeError:
            print("\t {0}: {1}".format(var, "***Unrecognized ASCII characters***"))
    print("\n")
    print("Variables in file: {list}".format(list=",".join(vars_dic.keys())))
    print("\n\n\n")

df.close()
