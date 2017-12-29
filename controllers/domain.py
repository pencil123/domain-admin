#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import sys
import os.path
import datetime

from base import BaseHandler
# from accesslog.module import Settings,Statistics
from utils.funs import pages
# from common.funs import aboutdate,date_range
from models.domain import Domain_model

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

domain_modle = Domain_model()


class DomainAdd(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		form_dict = domain_modle.kind_domain()
		self.render('domain/add.html',form_dict=form_dict)

	@tornado.web.authenticated
	def post(self):
		add_dict = {}
		for key in self.request.arguments:
			if key in set(['user','route','own','https']):
				value = self.get_argument(key)
				add_dict[key] = int(value)
			elif key in set(['domain','mark']):
				value = self.get_argument(key)
				add_dict[key] = value.encode('utf8')
			else:
				continue
		domain_modle.op_user(self.get_secure_cookie('account'))
		if domain_modle.single_add(add_dict):
			redict_url = "/domain/select?dom=%s&action=add" % (add_dict['domain'])
			self.redirect(redict_url)
		return None

class DomainSelect(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		try:
			dom = self.get_argument('dom')
		except:
			dom = 0
		if not dom:
			self.render('domain/select.html',dom=None,mesg=None)
			return None

		try:
			action = self.get_argument('action')
			if action == 'add':
				message = "域名添加成功"
			elif action == 'update':
				message = "域名更新成功"
		except:
			message =None

		count = domain_modle.items_count({'domain':dom.encode('utf8')})

		form_dict = domain_modle.kind_domain()

		if count != 1:
			self.render('domain/notfound.html',num_domain=count)
			return None

		dom_info = domain_modle.single_info(dom)

		dom_dict = {}
		dom_dict['id'] = dom_info[0]
		dom_dict['domain'] = dom_info[1]
		dom_dict['user'] = form_dict['user'][dom_info[2]]
		dom_dict['route'] = form_dict['route'][dom_info[3]]
		dom_dict['own'] = form_dict['own'][dom_info[4]]
		dom_dict['https'] = form_dict['https'][dom_info[5]]
		dom_dict['mark'] = dom_info[6]
		self.render('domain/select.html',dom=dom_dict,mesg = message)

class DomainUpdate(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		try:
			dom = self.get_argument('dom')
		except:
			dom = 0
		if not dom:
			self.redirect('/domain/select')

		#修改表单的默认项
		form_dict = domain_modle.kind_domain()
		dom_info = domain_modle.single_info(dom)

		form_dict['user']['default'] = dom_info[2]
		form_dict['route']['default'] = dom_info[3]
		form_dict['own']['default'] = dom_info[4]
		form_dict['https']['default'] = dom_info[5]

		dom_dict = {}
		dom_dict['id'] = dom_info[0]
		dom_dict['domain'] = dom_info[1]
		dom_dict['user'] = form_dict['user'][dom_info[2]]
		dom_dict['route'] = form_dict['route'][dom_info[3]]
		dom_dict['own'] = form_dict['own'][dom_info[4]]
		dom_dict['https'] = form_dict['https'][dom_info[5]]
		dom_dict['mark'] = dom_info[6]

		self.render('domain/update.html',dom=dom_dict,form_dict=form_dict)

	def post(self):
		change_dict = {}
		for key in self.request.arguments:
			if key in set(['user','route','own','https']):
				value = self.get_argument(key)
				change_dict[key] = int(value)
			elif key in set(['domain','mark']):
				value = self.get_argument(key)
				change_dict[key] = value.encode('utf8')
			else:
				continue
		domain_modle.op_user(self.get_secure_cookie('account'))
		if domain_modle.single_update(change_dict):
			redict_url = "/domain/select?dom=%s&action=update" % (change_dict['domain'])
			self.redirect(redict_url)
		return None


class DomainList(BaseHandler):
	'''
	list verbs  
	'''
	@tornado.web.authenticated
	def get(self):

		select_args = {}
		form_dict = domain_modle.kind_domain()

		#获取传参
		#1、搜索条件
		#2、form表单的记忆功能
		#3、pages翻页
		pages_pre = ""
		current_page = 1
		for key in self.request.arguments:
			if key == 'page':
				current_page = int(self.get_argument('page'))
				continue
			elif key in set(['route','own','https']):
				value = self.get_argument(key)
				form_dict[key]['default'] = int(value)
				pages_pre += "%s=%s&" % (key,value)
			elif key == 'user':
				value = self.get_argument(key)
				form_dict[key] = int(value)
				pages_pre += "%s=%s&" % (key,value)
			else:
				continue
			if value != '0':
				select_args[key] = value

		#默认页，不展示域名列表；没有翻页内容
		if not select_args:
			self.render('domain/index.html',Stats=None,form_dict=form_dict,pages_list=None)
			return None

		#域名列表内容
		domains = domain_modle.list(select_args,current_page)
		stat_list = []
		for num in range(len(domains)):
			single = domains[num]
			stat_dict = {}
			stat_dict['id'] = single[0]
			stat_dict['domain'] = single[1]
			stat_dict['route'] = form_dict['route'][single[3]]
			stat_dict['own'] = form_dict['own'][single[4]]
			stat_dict['https'] = form_dict['https'][single[5]]
			stat_dict['mark'] = single[6]
			stat_list.append(stat_dict)

		#翻页内容
		items_count = domain_modle.items_count(select_args)

		pages_list = []
		first_page = "?%spage=%s" % (pages_pre,1)
		pages_list.append(first_page)
		pages_list.append(current_page)
		pages_nums = pages(items_num=items_count,current_page=current_page)

		for num in range(len(pages_nums)):
			url_string = "?%spage=%s" % (pages_pre,pages_nums[num])
			pages_list.append(url_string)

		self.render('domain/index.html',Stats=stat_list,form_dict=form_dict,pages_list=pages_list)