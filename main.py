#!/usr/bin/env python

# https://www.pythoncentral.io/introduction-to-sqlite-in-python/
import sqlite3
import json
import time
import os.path
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
cursor = db.cursor()
cursor.execute('SELECT SQLITE_VERSION()')
print('version:', cursor.fetchone())


# Create table
def create_table(cursor):
	sql = '''CREATE TABLE IF NOT EXISTS {} 
			(id INTEGER PRIMARY KEY, block INTEGER, day INTEGER, year INTEGER, scheduleId TEXT, slideId TEXT, updatedTime INTEGER);'''.format(TABLE_NAME)
	cursor.execute(sql)
	print("Created table succesfully")

create_table(cursor)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# Drop
def drop_table(cursor, tablename):
	sql = '''DROP TABLE {0}'''.format(tablename)
	cursor.execute(sql)

# drop_table(cursor, "data")

# Insert Data
def insert_data(cursor):
	start_time = time.time()
	cursor.executemany("INSERT INTO data (block, day, year, scheduleId, slideId, updatedTime) VALUES (:block,:day,:year,:scheduleId,:slideId,:updatedTime);", datastore)
	db.commit()
	print("insert_data --- %s seconds ---" % (time.time() - start_time))

def print_table(cursor, tablename):
	start_time = time.time()
	print("\nEntire database contents:\n")
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	print(cursor.fetchall())
	# for row in cursor.execute("SELECT * FROM {0};".format(tablename)):
	cursor.execute("SELECT * FROM {0};".format(tablename))
	print(len(cursor.fetchall()))
	print("--- %s seconds ---" % (time.time() - start_time))
	
# print_table(cursor, "data")

print(cursor.execute("SELECT COUNT(*) FROM data").fetchone()[0])
# print('Last row id: %d' % cursor.lastrowid)


cur_request_day = 1
interval_request_day = 3

# Fetch data every 5m to test network and fetch
def fetch_data():
	start_time = time.time()
	print("\nFetch Schedule Blocks At Date \n")

	url = 'https://neuraldisplay-admin-api.herokuapp.com/test/blocks'

	querystring = {'days': [111, 112]}

	res = rq.get(url, params=querystring)
	print(res.url)
	print(res.status_code)
	
	res_json = res.json()
	print("fetch_data --- %s seconds ---" % (time.time() - start_time))
	return res_json

fetch_data()

# Save to DB
# Retreive from DB
# Repeat

def get_schedule_by_date(cursor, date):
	start_time = time.time()
	print("\nGet Schedule Blocks At Date: {}\n".format(date))
	sql = '''SELECT * FROM data WHERE day={};'''.format(date)
	cursor.execute(sql)
	print(len(cursor.fetchall()))
	print("get_schedule --- %s seconds ---" % (time.time() - start_time))

get_schedule_by_date(cursor, 112)

# Done
cursor.close()
db.close()