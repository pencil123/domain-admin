#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import logging

DEBUG = True
Port = '8080'
SECRET_KEY = 'HelloWorld'


settings = dict(
	cookie_secret = SECRET_KEY,
	login_url = '/login',
	template_path = os.path.join(os.path.dirname(__file__),"templates"),
	static_path = os.path.join(os.path.dirname(__file__),"static"),
	root_path = os.path.dirname(__file__),
	xsrf_cookies = False,
	autoescape = "xhtml_escape",
	debug = DEBUG,
	xheaders = True,
	)

LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO