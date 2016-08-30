#!/bin/bash

# Purpose:
#       Script to run EcoRAIDMooringMetaData2ptr for each grouping of deployments


prog_dir="/Volumes/WDC_internal/Users/bell/Programs/Python/EcoFOCI_PavlofMetaDB/"
out_dir="/Volumes/WDC_internal/Users/bell/scratch/"
sys_path="/home/ecoraid/data"


### Chukchi ###
###
#
# 2014
#
###
year=2014
ID='14chukchi1'
sites='14ckp1a 14ckt1a 14ckip1a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='14chukchi2'
sites='14ckp2a 14ckt2a 14ckip2a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='14chukchi4'
sites='14ckp4a 14ckt4a 14ckip4a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='14chukchi5'
sites='14ckp5a 14ckt5a 14ckip5a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='14chukchi6'
sites='14ckp6a 14ckt6a 14ckip6a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='14chukchi7'
sites='14ckp7a 14ckt7a 14ckip7a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='14chukchi8'
sites='14ckp8a 14ckt8a 14ckip8a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='14chukchi9'
sites='14ckp9a 14ckt9a 14ckip9a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

###
#
# 2013
#
###
year=2013
ID='13chukchi1'
sites='13ckp1a 13ckt1a 13ckip1a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='13chukchi2'
sites='13ckp2a 13ckt2a 13ckip2a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='13chukchi4'
sites='13ckp4a 13ckt4a 13ckip4a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='13chukchi5'
sites='13ckp5a 13ckt5a 13ckip5a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='13chukchi6'
sites='13ckp6a 13ckt6a 13ckip6a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='13chukchi7'
sites='13ckp7a 13ckt7a 13ckip7a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

###
#
# 2012
#
###
year=2012

ID='12chukchi2'
sites='12ckp2a 12ckt2a 12ckip2a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='12chukchi4'
sites='12ckp4a 12ckt4a 12ckip4a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

###
#
# 2011
#
###
year=2011

ID='11chukchi1'
sites='11ckp1a 11ckt1a 11ckip1a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='11chukchi2'
sites='11ckp2a 11ckt2a 11ckip2a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

ID='11chukchi3'
sites='11ckp3a 11ckt3a 11ckip3a'
python ${prog_dir}EcoRAIDMooringMetaData2ptr.py ${ID} ${year} ${sys_path} ${sites} >> ${out_dir}${ID}.ptr

