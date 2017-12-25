#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from accesslog.module import Settings

class Page():
	def __init__(self,cls_name='',current_page=1):
		self.current_page = current_page
		self.cls_name = cls_name
		self.page_size = 30

		if self.cls_name == "dateslistdomain":
			self.handler = DailyHandler()
		elif self.cls_name == "clientaddrchina":
			self.handler = ClientAddrChinaHandler()
		elif self.cls_name == "agentsfrom":
			self.handler = AgentsFromHandler()
		elif self.cls_name == "hostlist":
			self.handler = HostHandler()
		elif self.cls_name == "verbslist":
			self.handler = VerbHandler()
		elif self.cls_name == "requesttimepercentiler":
			self.handler = RequestTimePerHandler()
		elif self.cls_name == "statuslist":
			self.handler = StatusHandler()
		else:
			self.handler = DomainsHandler(self.cls_name)


	def get_items(self):

		num_start = (self.current_page-1) * self.page_size
		num_end = self.current_page * self.page_size
		items_list = self.handler.selectlimit(start=num_start,end=num_end)
		return items_list

	def get_pages(self,pre_url=""):
		pre_url = "<a href=" + pre_url

		num_items = self.handler.docs_count()

		num_page = num_items/self.page_size+1 if num_items%self.page_size \
		else num_items/self.page_size
		
		first_page = pre_url + "?page=1>First</a>"
		pre_page = pre_url + "?page=" + str(self.current_page-1) + ">Previous</a>"
		next_page = pre_url + "?page=" + str(self.current_page+1) + ">Next</a>"
		last_page = pre_url + "?page=" + str(num_page) + ">Last</a>"

		if self.current_page == 1:
			pre_page = "Hello"
		if self.current_page == num_page:
			next_page = "World"
			
		pages = first_page + " <>#<> " + pre_page + " <>#<> " + next_page + " <>#<> " + last_page
		return pages
