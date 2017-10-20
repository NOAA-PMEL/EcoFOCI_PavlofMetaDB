#!/usr/bin/env python

"""
 Background:
 --------
 EcoFOCI_db_io.py
 
 
 Purpose:
 --------
 Various Routines and Classes to interface with the mysql database that houses EcoFOCI meta data
 
  History:
 --------
 2017-07-28 S.Bell - replace pymsyql with mysql.connector -> provides purepython connection and prepared statements

"""

import mysql.connector
import ConfigParserLocal 
import datetime
import numpy as np

__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2017, 7, 28)
__modified__ = datetime.datetime(2017, 7, 28)
__version__  = "0.2.0"
__status__   = "Development"
__keywords__ = 'netCDF','meta','header','pymysql'

class NumpyMySQLConverter(mysql.connector.conversion.MySQLConverter):
	""" A mysql.connector Converter that handles Numpy types """

	def _float32_to_mysql(self, value):
		if np.isnan(value):
			return None
		return float(value)

	def _float64_to_mysql(self, value):
		if np.isnan(value):
			return None
		return float(value)

	def _int32_to_mysql(self, value):
		if np.isnan(value):
			return None
		return int(value)

	def _int64_to_mysql(self, value):
		if np.isnan(value):
			return None
		return int(value)

class EcoFOCI_db_datastatus(object):
	"""Class definitions to access EcoFOCI Mooring Database"""

	def connect_to_DB(self, db_config_file=None, ftype='yaml'):
		"""Try to establish database connection

		Parameters
		----------
		db_config_file : str
			full path to json formatted database config file    

		"""
		db_config = ConfigParserLocal.get_config(db_config_file,ftype=ftype)
		try:
			self.db = mysql.connector.connect(**db_config)
		except mysql.connector.Error as err:
		  """
		  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		  elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		  else:
			print(err)
		  """
		  print("error - will robinson")
		  
		self.db.set_converter_class(NumpyMySQLConverter)

		# prepare a cursor object using cursor() method
		self.cursor = self.db.cursor(dictionary=True)
		self.prepcursor = self.db.cursor(prepared=True)
		return(self.db,self.cursor)

	def manual_connect_to_DB(self, host='localhost', user='viewer', 
							 password=None, database='ecofoci', port=3306):
		"""Try to establish database connection

		Parameters
		----------
		host : str
			ip or domain name of host
		user : str
			account user
		password : str
			account password
		database : str
			database name to connect to
		port : int
			database port

		"""
		db_config = {}     
		db_config['host'] = host
		db_config['user'] = user
		db_config['password'] = password
		db_config['database'] = database
		db_config['port'] = port

		try:
			self.db = mysql.connector.connect(**db_config)
		except:
			print "db error"
			
		# prepare a cursor object using cursor() method
		self.cursor = self.db.cursor(dictionary=True)
		self.prepcursor = self.db.cursor(prepared=True)
		return(self.db,self.cursor)

	def read_table(self, table=None, verbose=False, index_str='id', **kwargs):
		"""build sql call based on kwargs"""

		if ('mooringid' in kwargs.keys()) and ('year' in kwargs.keys()):
			sql = ("SELECT * FROM `{0}` WHERE `mooringid`='{1}' and `year`={2}").format(table, kwargs['mooringid'], kwargs['year'])
		elif 'year' in kwargs.keys():
			sql = ("SELECT * FROM `{0}` WHERE `year`={1}").format(table, kwargs['year'])
		elif 'mooringid' in kwargs.keys():
			sql = ("SELECT * FROM `{0}` WHERE `mooringid`='{1}'").format(table, kwargs['mooringid'])
		else:
			sql = ("SELECT * FROM `{0}` ").format(table)

		if verbose:
			print sql


		result_dic = {}
		try:
			self.cursor.execute(sql)
			for row in self.cursor:
				result_dic[row[index_str]] ={keys: row[keys] for val, keys in enumerate(row.keys())} 
			return (result_dic)
		except:
			print "Error: unable to fecth data"

	def read_mooring_summary(self, table=None, verbose=False, **kwargs):
		""" output is mooringID indexed """
		if 'mooringid' in kwargs.keys():
			sql = ("SELECT * FROM `{0}` WHERE `MooringID`='{1}'").format(table, kwargs['mooringid'])
		elif 'deployed' in kwargs.keys():
			sql = ("SELECT * FROM `{0}` WHERE `DeploymentStatus`='DEPLOYED'").format(table)
		else:
			sql = ("SELECT * FROM `{0}` ").format(table)

		if verbose:
			print sql

		result_dic = {}
		try:
			self.cursor.execute(sql)
			for row in self.cursor:
				result_dic[row['MooringID']] ={keys: row[keys] for val, keys in enumerate(row.keys())} 
			return (result_dic)
		except:
			print "Error: unable to fecth data"

	def read_mooring_inst(self, table=None, verbose=False, mooringid=None, isdeployed='y'):
		"""specific to get deployed instruments"""
		sql = ("SELECT * from `{0}` WHERE `MooringID`='{1}' AND `Deployed` = '{2}' Order By `Depth`").format(table, mooringid, isdeployed)

		if verbose:
			print sql

		result_dic = {}
		try:
			self.cursor.execute(sql)
			for row in self.cursor:
				result_dic[row['InstType']+row['SerialNo']] ={keys: row[keys] for val, keys in enumerate(row.keys())} 
			return (result_dic)
		except:
			print "Error: unable to fecth data"

	def close(self):
		"""close database"""
		self.prepcursor.close()
		self.cursor.close()
		self.db.close()
		
class EcoFOCI_db_ProfileData(object):
	"""Class definitions to access EcoFOCI Profile Data Database"""

	def connect_to_DB(self, db_config_file=None,ftype='yaml'):
		"""Try to establish database connection

		Parameters
		----------
		db_config_file : str
			full path to json formatted database config file    

		"""
		self.db_config = ConfigParserLocal.get_config(db_config_file,ftype=ftype)
		try:
			self.db = mysql.connector.connect(self.db_config['host'], 
									  self.db_config['user'],
									  self.db_config['password'], 
									  self.db_config['database'], 
									  self.db_config['port'])
		except:
			print "db error"
			
		# prepare a cursor object using cursor() method
		self.cursor = self.db.cursor(mysql.connector.cursors.DictCursor)
		return(self.db,self.cursor)

	def manual_connect_to_DB(self, host='localhost', user='viewer', 
							 password=None, database='ecofoci', port=3306):
		"""Try to establish database connection

		Parameters
		----------
		host : str
			ip or domain name of host
		user : str
			account user
		password : str
			account password
		database : str
			database name to connect to
		port : int
			database port

		"""	    
		self.db_config['host'] = host
		self.db_config['user'] = user
		self.db_config['password'] = password
		self.db_config['database'] = database
		self.db_config['port'] = port

		try:
			self.db = mysql.connector.connect(self.db_config['host'], 
									  self.db_config['user'],
									  self.db_config['password'], 
									  self.db_config['database'], 
									  self.db_config['port'])
		except:
			print "db error"
			
		# prepare a cursor object using cursor() method
		self.cursor = self.db.cursor(mysql.connector.cursors.DictCursor)
		return(self.db,self.cursor)

	def read_profile(self, table=None, ProfileID=None, verbose=False):
		
		sql = ("SELECT * from `{0}` WHERE `ProfileID`= '{1}' ORDER BY `id` DESC ").format(table, ProfileID)

		if verbose:
			print sql

		result_dic = {}
		try:
			# Execute the SQL command
			self.cursor.execute(sql)
			# Get column names
			rowid = {}
			counter = 0
			for i in self.cursor.description:
				rowid[i[0]] = counter
				counter = counter +1 
			#print rowid
			# Fetch all the rows in a list of lists.
			results = self.cursor.fetchall()
			for row in results:
				result_dic[row['dep']] ={keys: row[keys] for val, keys in enumerate(row.keys())} 
			return (result_dic)
		except:
			print "Error: unable to fetch data"

	def count(self, table=None, start=None, end=None, verbose=False):
		sql = ("SELECT count(*) FROM (SELECT * FROM `{table}` where ProfileID between"
			   " '{start}' and '{end}' group by `ProfileID`) as temp").format(table=table, start=start, end=end)

		if verbose:
			print sql	

		try:
			# Execute the SQL command
			self.cursor.execute(sql)
			# Get column names
			rowid = {}
			counter = 0
			for i in self.cursor.description:
				rowid[i[0]] = counter
				counter = counter +1 
			#print rowid
			# Fetch all the rows in a list of lists.
			results = self.cursor.fetchall()
			return results[0]['count(*)']
		except:
			print "Error: unable to fetch data"

	def get_distance(self, ref_lat, ref_lon, ProfileID_end):
		sql = """SELECT (
		  6371 * acos(
			cos(radians({ref_lat})) * cos(radians(x(LatitudeLongitude))) * cos(radians(y(LatitudeLongitude)) - radians({ref_lon}))
			+
			sin(radians({ref_lat})) * sin(radians(x(LatitudeLongitude)))
		  )
		) AS distance
		FROM dy1606 WHERE id={id};""".format(ref_lat=ref_lat,ref_lon=ref_lon,id=ProfileID_end)

		try:
			# Execute the SQL command
			self.cursor.execute(sql)
			# Get column names
			rowid = {}
			counter = 0
			for i in self.cursor.description:
				rowid[i[0]] = counter
				counter = counter +1 
			#print rowid
			# Fetch all the rows in a list of lists.
			results = self.cursor.fetchall()
			return results[0]['distance']
		except:
			print "Error: unable to fetch data"

	def create_table(self, tablename, vars_list):

		sql = """CREATE TABLE `{tablename}` (
			  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
			  `ProfileID` varchar(6) DEFAULT '' COMMENT 'ctdxxx',
			  `ProfileTime` datetime DEFAULT NULL,
			  `DataStatus` enum('preliminary','final') NOT NULL DEFAULT 'preliminary',
			  `LatitudeLongitude` point DEFAULT NULL,""".format(tablename=tablename)

		for varname in vars_list:
			if not varname in ['time','time2']:
				sql = sql + """`{variable}` float DEFAULT NULL,""".format(variable=varname)

		sql = sql + """
			  PRIMARY KEY (`id`)
			) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;"""

		try:
			# Execute the SQL command
			self.cursor.execute(sql)
		except:
			print("Failed to create table")

	def add_ctd_profile(self, tablename, castno, data, datetime='0000-00-00 00:00:00', DataStatus='preliminary'):

		data.pop('time', None)
		data.pop('time2', None)
		lat = data.pop('lat', None)
		lon = data.pop('lon', None)

		placeholders = ', '.join(['%s'] * (len(data)+5)) + ', ST_GeomFromText(%s)' #lat,lon,time,castno,geom_latlon are added after data
		columns = ', '.join(data.keys() + ['lat','lon','ProfileTime','ProfileID','DataStatus','LatitudeLongitude'])

		sql = """INSERT INTO {tablename} ({columns}) VALUES({placeholders}) """.format(tablename=tablename,placeholders=placeholders,columns=columns)

		for rindex in range(0,len(data['dep'])):
			sql_data = []
			for k,v in data.iteritems():
				try:
					sql_data = sql_data + [str(data[k][0,rindex,0,0])]
				except:
					sql_data = sql_data + [str(data[k][rindex])]
			if 'ctd' in castno:
				sql_data = sql_data + [str(lat[0]),str(lon[0]),datetime,str(castno),DataStatus,'POINT('+str(lat[0])+' '+str(lon[0])+')']
			else:
				sql_data = sql_data + [str(lat[0]),str(lon[0]),datetime,'ctd'+str(castno),DataStatus,'POINT('+str(lat[0])+' '+str(lon[0])+')']
			try:
				# Execute the SQL command
				self.cursor.execute(sql, sql_data)
				self.db.commit()
			except mysql.connector.Error as error: 
				print("Error: {}".format(error))
				self.db.rollback()

	def close(self):
		"""close database"""
		self.db.close()