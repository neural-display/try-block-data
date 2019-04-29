#!/bin/bash

sudo apt-get update && sudo apt-get upgrade

sudo apt-get install sqlite3

sqlite3 --version

sqlite3 test.db

