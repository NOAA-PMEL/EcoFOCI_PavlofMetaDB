#!/bin/bash

# Purpose:
#       Script to run EcoRAIDMooringMetaData2ptr for each grouping of deployments


prog_dir="/Volumes/WDC_internal/Users/bell/Programs/Python/EcoFOCI_PavlofMetaDB/"
data_dir="/Volumes/WDC_internal/Users/bell/ecoraid/2016/CTDcasts/cf1601/final_data/ctd/*.nc"


first_cast=0
for files in $data_dir
do
	if [ ${first_cast} -eq 0 ]
	then
		echo "Adding new table based on :$files"
		echo "processing file: $files"
		python ${prog_dir}EcoFOCI_NetCDF2DB.py ${files} -c
		python ${prog_dir}EcoFOCI_NetCDF2DB.py ${files} -f
		first_cast=1
	else
		echo "processing file: $files"
		python ${prog_dir}EcoFOCI_NetCDF2DB.py ${files} -f
	fi
done

