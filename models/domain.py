#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# from models.sqlite import sqlite_handler
import sqlite3
import ast
import types
import datetime
from utils.funs import tostr
sqlite_handler = sqlite3.connect('/www/domains.db')
sqlite_handler.text_factory = str

# create table domain(
# id integer primary key autoincrement,
# domain varchar(50),
# user tinyint unsigned,
# route tinyint unsigned,
# own tinyint unsigned,
# https tinyint unsigned,
# mark varchar(30)
# );

class Domain_model(object):
	def __init__(self):
		self.cursor_handler = sqlite_handler.cursor()

	def op_user(self,username):
		self.user = username

	def list(self,where_dict={},page=1):
		First_num = True
		# print where_dict
		where_sql = ''
		for (k,v) in where_dict.items():
			if First_num:
				if type(v) is types.StringType:
					where_sql += "%s = '%s' " % (k,v)
				else:
					where_sql += "%s = %s " % (k,v)
				First_num = False
			else:
				if type(v) is types.StringType:
					where_sql += "and %s = '%s' " % (k,v)
				else:
					where_sql += "and %s = %s " % (k,v)
		items_start = int(page) -1
		string = "select id,domain,user,route,own,https,mark from domain where %s order by id asc limit %s,20" % (where_sql,items_start*20)
		sql_string = tostr(string)
		self.cursor_handler.execute(sql_string)
		result = self.cursor_handler.fetchall()
		return result

	def items_count(self,where_dict={}):
		First_num = True
		where_sql = ''
		for (k,v) in where_dict.items():
			print type(v)
			if First_num:
				if type(v) is types.StringType:
					where_sql += "%s = '%s' " % (k,v)
				else:
					where_sql += "%s = %s " % (k,v)
				First_num = False
			else:
				if type(v) is types.StringType:
					where_sql += "and %s = '%s' " % (k,v)
				else:
					where_sql += "and %s = %s " % (k,v)

		string = "select count(*) from domain where %s" % (where_sql,)
		sql_string = tostr(string)

		self.cursor_handler.execute(sql_string)
		result = self.cursor_handler.fetchone()
		return result[0]

	def kind_domain(self):
		kind_dict = {}
		string = "select parameter,supplement from settings where setting = 'kind_domain'"
		sql_string = tostr(string)
		self.cursor_handler.execute(sql_string)
		result = self.cursor_handler.fetchall()

		for num in range(len(result)):
			single = result[num]
			if kind_dict.has_key(single[0]):
				kind_dict[single[0]].update(ast.literal_eval(single[1]))
			else:
				kind_dict[single[0]] = {0:'Not Set'}
				kind_dict[single[0]].update(ast.literal_eval(single[1]))

		return kind_dict

	def single_info(self,domain):
		string = "select id,domain,user,route,own,https,mark from domain where domain = '%s'" % (domain,)
		sql_string = tostr(string)
		self.cursor_handler.execute(sql_string)
		result = self.cursor_handler.fetchone()
		return result

	def single_add(self,add_dict):
		First_num = True
		key_string = ''
		value_string = ''
		for (k,v) in add_dict.items():
			print k,v
			if First_num:
				key_string += "%s" % (k)
				if type(v) is types.StringType:
					value_string += "'%s'" % (v)
				else:
					value_string += "%s" % (v)
				First_num = False
			else:
				key_string += ",%s" % (k)
				if type(v) is types.StringType:
					value_string += ",'%s' " % (v)
				else:
					value_string += ",%s " % (v)

		string = "insert into domain (%s) values(%s)" % (key_string,value_string)
		sql_string = tostr(string)
		time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		log_string = "insert into log (username,datetime,operation) values(?,?,?)"
		log_string = tostr(log_string)
		log_value = (self.user,time_str,sql_string)
		self.cursor_handler.execute(sql_string)
		self.cursor_handler.execute(log_string,log_value)
		sqlite_handler.commit()
		return True

	def single_update(self,update_dict):
		First_num = True
		update_sql = ''
		for (k,v) in update_dict.items():
			print k,v
			if k == 'domain':
				continue
			print type(v)
			if First_num:
				if type(v) is types.StringType:
					update_sql += "%s = '%s' " % (k,v)
				else:
					update_sql += "%s = %s " % (k,v)
				First_num = False
			else:
				if type(v) is types.StringType:
					update_sql += ",%s = '%s' " % (k,v)
				else:
					update_sql += ",%s = %s " % (k,v)

		string = "update domain set %s where domain = '%s'" % (update_sql,update_dict['domain'])
		sql_string = tostr(string)
		time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		log_string = "insert into log (username,datetime,operation) values(?,?,?)"
		log_string = tostr(log_string)
		log_value = (self.user,time_str,sql_string)
		self.cursor_handler.execute(sql_string)
		self.cursor_handler.execute(log_string,log_value)
		sqlite_handler.commit()
		return True