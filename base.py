#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		user = self.get_secure_cookie('account')
		if user:
			return user
		else:
			return False