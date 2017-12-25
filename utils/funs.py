#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import hashlib
import datetime
def md5(raw_string):
	return hashlib.md5(raw_string).hexdigest()

def tostr(sql_string):
	if isinstance(sql_string,unicode):
		return sql_string.encode('utf8')
	else:
		return sql_string

def date_range(string_date):
	'''
	parameter string_date "YYYY-MM-DD"
	return list date "YYYY-MM-DD 00.00.000" 
	'''
	TimeRange = []
	time_from = string_date + " 00:00:01"
	time_to = string_date + " 23:59:59"
	TimeRange.append(time_from)
	TimeRange.append(time_to)
	return TimeRange

def aboutdate(string_date):
	'''
	@parameter get the string type date
	@return dict previous current next
	'''
	url_date = {}

	current_date = datetime.datetime.strptime(string_date,"%Y-%m-%d")
	previous_date = current_date + datetime.timedelta(days = -1)
	next_date = current_date + datetime.timedelta(days = 1)

	url_date['current'] = current_date.strftime('%Y-%m-%d')
	url_date['previous'] = previous_date.strftime('%Y-%m-%d')
	url_date['next'] = next_date.strftime('%Y-%m-%d')
	return url_date

def pages(page_size=20,current_page=0,items_num=0):
	'''返回4个数字；
	上一页
	下一页
	最后页'''
	last_page = items_num/page_size+1 if items_num%page_size else items_num/page_size
	next_page = current_page+1 if current_page+1<=last_page else last_page
	pre_page = current_page-1 if current_page -1 >=1 else 1
	return (pre_page,next_page,last_page)