#!/usr/bin/env

"""
 OutputDBMooringLocation.py
 
 Purpose:
 --------

 Output the GeoLocation of EcoFOCI Mooring Sites archived in the EcoFOCI 
 	Mooring Deployment database.

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
__created__  = datetime.datetime(2016, 9, 7)
__modified__ = datetime.datetime(2016, 9, 7)
__version__  = "0.1.0"
__status__   = "Development"

"""------------------------------------------------------------------------------------"""

#TODO: Move classes below to seperate tools

class MooringGeoLoc(object):
	
	def __init__(self, db_data=None):
		""" Take the id indexed output from the database and convert it to a simple
				dictionary of {mooringid: {lat, lon}}
        Parameters
        ----------
        db_data : dictionary
            dictionary indexed by database "id" key.  Must contain "Latitude, Longitude, MooringID"

	    Returns
    	-------
		dictionary.
		"""
		dicdata={}
		for i in db_data.keys():
			MooringID = db_data[i]['MooringID']
			dicdata[MooringID] = {'Latitude': db_data[i]['Latitude'], 
								  'Longitude':db_data[i]['Longitude'],
								  'PreLatitude': db_data[i]['PreLatitude'], 
								  'PreLongitude':db_data[i]['PreLongitude']}
		self.dicdata = dicdata
		
	def get_geoloc_data(self):
		"""return the initialized thin dictionary"""
		return(self.dicdata)

	def LatLonDM2DD(self, lonpos='W', latpos='N',omit_missing=True):
		"""latitude longitude conversion
		Converts from:
		DD MM.MM -> DD.ddd

		Paramters
		---------
		self.dicdata : dictionary of dictionaries in which the primary index is the 
			mooring id, the embedded dictionaries contain latitude and longitude as strings
		lonpos : str
			direction of positive longitude axis
			default : + west

		latpos : str
			direction of positive latitude axis
			default : + north

		omit_missing : bool
			True : skip moorings that were not deployed or have no position information
			False : keep moorings that were not deployed or lack position info

		"""
		for i in self.dicdata.keys():
			templat = self.dicdata[i]['Latitude'].strip().split()
			try:
				if templat[2] == latpos:
					self.dicdata[i]['Latitude'] = float(templat[0]) + float(templat[1]) / 60.
				else:
					self.dicdata[i]['Latitude'] = -1. * ( float(templat[0]) + float(templat[1]) / 60. )
			except:
				try:
					templat = self.dicdata[i]['PreLatitude'].strip().split()
					if not templat and omit_missing:
						self.dicdata.pop(i, None)
						continue
					elif not templat and not omit_missing:
						continue
					elif templat[2] == latpos:
						self.dicdata[i]['Latitude'] = float(templat[0]) + float(templat[1]) / 60.
					else:
						self.dicdata[i]['Latitude'] = -1. * ( float(templat[0]) + float(templat[1]) / 60. )
				except:
					self.dicdata.pop(i, None)
					continue

			templon = self.dicdata[i]['Longitude'].strip().split()
			try:
				if templon[2] == lonpos:
					self.dicdata[i]['Longitude'] = float(templon[0]) + float(templon[1]) / 60.
				else:
					self.dicdata[i]['Longitude'] = -1. * ( float(templon[0]) + float(templon[1]) / 60. )
			except:
				try:
					templon = self.dicdata[i]['PreLongitude'].strip().split()
					if not templon and omit_missing:
						self.dicdata.pop(i, None)
						continue
					elif not templon and not omit_missing:
						continue
					elif templon[2] == lonpos:
						self.dicdata[i]['Longitude'] = float(templon[0]) + float(templon[1]) / 60.
					else:
						self.dicdata[i]['Longitude'] = -1. * ( float(templon[0]) + float(templon[1]) / 60. )
				except:
					self.dicdata.pop(i, None)
					continue

	def output_csv(self):
		"""sort and output to screen"""
		print "MooringID,Latitude,Longitude"
		for i in sorted(self.dicdata.keys()):
			print "{mooringid},{Latitude},{Longitude}".format(mooringid=i, **self.dicdata[i])

	def output_csv_tableau(self):
		"""Initially inteded for a tableau visualization.  The purpose is to identify the collection of
		individual moorings deployed at a consistent site location.

		TODO:

		"""
		#get the official desginatio of the mooring without the year id
		pass

	def output_kml(self):
		"""TODO: output data in kml friendly format for GoogleEarth"""
		pass

	def output_geojson(self):
		for i in sorted(self.dicdata.keys())[:-1]:
			print ('{{ "type":"Feature","geometry": {{ "type": "Point", "coordinates": [{Longitude},{Latitude}]}},"properties": {{"MooringID":"{mooringid}"}}}},').format(mooringid=i, **self.dicdata[i])
		else:
			i = sorted(self.dicdata.keys())[-1]
			print ('{{ "type":"Feature","geometry": {{ "type": "Point", "coordinates": [{Longitude},{Latitude}]}},"properties": {{"MooringID":"{mooringid}"}}}}').format(mooringid=i, **self.dicdata[i])

"""------------------------------------------------------------------------------------"""
parser = argparse.ArgumentParser(description='MySQL database --> geolocation file')
parser.add_argument('-kml', '-kml', 
	action="store_true", 
	help='output as kml file')
parser.add_argument('-csv', '-csv', 
	action="store_true", 
	help='output as csv file')
parser.add_argument('-geojson', '-geojson', 
	action="store_true", 
	help='output as geojson file')


args = parser.parse_args()


EcoFOCI_db = EcoFOCI_db_datastatus()
config_file = 'EcoFOCI_config/db_config/db_config_mooring.pyini'
(db,cursor) = EcoFOCI_db.connect_to_DB(db_config_file=config_file)
data = EcoFOCI_db.read_table(table='mooringdeploymentlogs')
EcoFOCI_db.close()

if args.csv:
	instance = MooringGeoLoc(data)
	instance.LatLonDM2DD(lonpos='E')
	instance.output_csv()

if args.geojson:
	instance = MooringGeoLoc(data)
	instance.LatLonDM2DD(lonpos='E')

	header = """{  "type": "FeatureCollection", "features": [ """
	print "{header}".format(header=header)
	
	instance.output_geojson()

	footer = """  ]	} """
	print "{footer}".format(footer=footer)

if args.kml:
	print "Not currently functioning"


