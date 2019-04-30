#!/usr/bin/env python

# https://www.pythoncentral.io/introduction-to-sqlite-in-python/
import sqlite3
import json
import time
import os.path
import random

import requests as rq


DB_NAME = "test.db"
TABLE_NAME = "data"

# SQL File with Table Schema and Initialization Data
SQL_FILE_NAME = "test.sql"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

start_time = time.time()
# Open JSON file as datasource
TEST_DATA = "response.json"
with open(TEST_DATA, encoding='utf-8') as json_file:
	datastore = json.load(json_file)
	# print(datastore)

print("--- %s seconds ---" % (time.time() - start_time))

def create_or_open_db(filename):
	# file_exists = os.path.isfile(filename)
	DB_PATH = os.path.join(BASE_DIR, filename)
	print(DB_PATH)
	conn = sqlite3.connect(DB_PATH)
	if conn:
		print("{0} database successfully opened".format(filename))
	else:
		print("{0} database successfully created".format(filename))
	return conn

db = create_or_open_db(DB_NAME)
# Get a cursor object
_cursor = db.cursor()
_cursor.execute('SELECT SQLITE_VERSION()')
print('version:', _cursor.fetchone())


# Create table
def create_tables(cursor=_cursor):
	sql = '''CREATE TABLE IF NOT EXISTS {} 
			(id INTEGER PRIMARY KEY, 
			block INTEGER, day INTEGER, 
			year INTEGER, 
			scheduleId TEXT, 
			slideId TEXT, 
			updatedTime INTEGER);
			'''.format(TABLE_NAME)
	cursor.execute(sql)
	print("Created table succesfully")

create_tables()

'''Check again to make sure tables exist'''
_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(_cursor.fetchall())

# Drop Table
def drop_table(cursor, tablename):
	sql = '''DROP TABLE {0}'''.format(tablename)
	cursor.execute(sql)

# drop_table(cursor, "data")

# Insert Data
def insert_data(data, cursor =_cursor):
	start_time = time.time()
	cursor.executemany('''INSERT INTO data (block, day, year, scheduleId, slideId, updatedTime) 
						VALUES (:block,:day,:year,:scheduleId,:slideId,:updatedTime);''', data)
	db.commit()
	print("insert_data --- %s seconds ---" % (time.time() - start_time))

# insert_data(datastore)

def print_table(cursor, tablename):
	start_time = time.time()
	print("\nEntire database contents:\n")
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	print(cursor.fetchall())

	# cursor.execute("SELECT * FROM {};".format(tablename))
	# print(len(cursor.fetchall()))

	'''Faster than len(cursor.fetchall())'''
	print(cursor.execute("SELECT COUNT(*) FROM {}".format(tablename)).fetchone()[0])
	print("--- %s seconds ---" % (time.time() - start_time))


# Fetch data every 5m to test network and fetch
def fetch_data(dates):
	start_time = time.time()
	print("\nFetch Schedule Blocks At Date \n")

	url = 'https://neuraldisplay-admin-api.herokuapp.com/test/blocks'

	querystring = {'days': dates}

	res = rq.get(url, params=querystring)
	print(res.url)
	print(res.status_code)
	
	res_json = res.json()
	# print(res_json)
	print("fetch_data --- %s seconds ---" % (time.time() - start_time))
	return res_json

# fetch_data([1])

'''
- Fetch datas
- Save to DB
- Repeat 30 days or request cocurrence 30 days
- Retreive from DB
'''
CACHED_DATES = 30

# cur_request_day = 1
interval_request_day = 2

start_time = time.time()
for i in range(1, CACHED_DATES, interval_request_day):
	req_range = range(i, i + interval_request_day)
	print('\nRequet date: {}'.format(list(req_range)))
	insert_data(fetch_data(req_range))

print("Recurrence request --- %s seconds ---" % (time.time() - start_time))




def get_schedule_by_date(cursor, date):
	start_time = time.time()
	print("\nGet Schedule Blocks At Date: {}".format(date))
	# sql = '''SELECT * FROM data WHERE day={};'''.format(date)
	# cursor.execute(sql)
	# print(len(cursor.fetchall()))

	sql = "SELECT COUNT(*) FROM data WHERE day={};".format(date)
	print(cursor.execute(sql).fetchone()[0])

	print("get_schedule --- %s seconds ---" % (time.time() - start_time))

get_schedule_by_date(_cursor, random.randint(1, CACHED_DATES))


print('\n------- Check and print all metrics again -------')
print_table(_cursor, "data")

# Done
_cursor.close()
db.close()