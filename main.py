#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import tornado.web

from base import BaseHandler


class IndexHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render('index.html')
		#self.render('common/logout.html')


class TestHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		name = tornado.escape.xhtml_escape(self.current_user)
		self.write("hello," +name)


# class LoginHandler(BaseHandler):
# 	def get(self):
# 		self.set_secure_cookie("account","Grey")
# 		# count = int(cookie) +1 if cookie else 1
# 		# countString = "1 time" if count ==1 else "%d times" % count
# 		# self.set_secure_cookie("count",str(count))
# 		self.render('index.html')