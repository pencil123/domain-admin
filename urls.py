#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import main
#import models.urls
import controllers.urls


urlpatterns = [
	(r"/?",main.IndexHandler),
	(r"/test",main.TestHandler),
]
urlpatterns += controllers.urls.urlpatterns