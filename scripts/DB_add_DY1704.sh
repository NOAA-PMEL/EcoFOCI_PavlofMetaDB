#!/bin/bash

# Purpose:
#       Script to run EcoRAIDMooringMetaData2ptr for each grouping of deployments


prog_dir="/Users/bell/Programs/Python/EcoFOCI_PavlofMetaDB/"
data_dir="/Users/bell/ecoraid/2017/CTDcasts/dy1704/initial_archive/*.nc"


first_cast=0
for files in $data_dir
do
	if [ ${first_cast} -eq 0 ]
	then
		echo "Adding new table based on :$files"
		echo "processing file: $files"
		python ${prog_dir}EcoFOCI_NetCDF2DB.py ${files} -c
		python ${prog_dir}EcoFOCI_NetCDF2DB.py ${files}
		first_cast=1
	else
		echo "processing file: $files"
		python ${prog_dir}EcoFOCI_NetCDF2DB.py ${files}
	fi
done

