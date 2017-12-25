#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import sys
import os.path
import random
import mongoengine

import tornado.httpserver
import tornado.ioloop
import tornado.web

import settings
from urls import urlpatterns


class Application(tornado.web.Application):
	def __init__(self):
		#指定url对应的handler；
		#调用tornado.web.Application类的init 函数
		tornado.web.Application.__init__(self,urlpatterns,**settings.settings)


if __name__ == "__main__":
	mongoengine.connect('daily', host='localhost', port=27017)
	http_server = tornado.httpserver.HTTPServer(Application())
	if settings.DEBUG:
		http_server.listen(settings.Port)
	else:
		http_server.bind(settings.Port)
		http_server.start(0)
	tornado.ioloop.IOLoop.instance().start()