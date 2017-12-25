#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# from models.sqlite import sqlite_handler
import sqlite3
from utils.funs import tostr
sqlite_handler = sqlite3.connect('/www/domains.db')

# /*create table user(
# id integer primary key autoincrement,
# name varchar(20),
# password varchar(20)
# );*/

class Auth_model(object):
	def __init__(self):
		self.cursor_handler = sqlite_handler.cursor()

	def check_login(self,username,password):
		string = "select count(*) from user where name='%s' and password='%s'" % (username,password)
		sql_string = tostr(string)
		self.cursor_handler.execute(sql_string)
		result = self.cursor_handler.fetchone()
		if result[0] == 0:
			return False
		elif result[0] == 1:
			return True
		else:
			return False

	def register(self,username,password):
		string = "insert into user(name,password) values('%s','%s')" % (username,password)
		sql_string = tostr(string)
		try:
			self.cursor_handler.execute(sql_string)
			sqlite_handler.commit()
		except sqlite3.IntegrityError:
			return False
		except:
			return False
		return True

# create table settings (
# 	setting varchar(20),
# 	parameter varchar(20),
#	supplement varchar(20)
# 	);
	def register_code(self,register_code):
		string = "select count(*) from settings where setting = '%s' and parameter ='%s'" % ('register_code',register_code)
		sql_string = tostr(string)
		self.cursor_handler.execute(sql_string)
		result = self.cursor_handler.fetchone()
		if result[0] == 0:
			return False
		elif result[0] == 1:
			return True
		else:
			return False