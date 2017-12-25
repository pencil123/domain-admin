#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from controllers.auth import LoginHandler,RegisterHandler
from controllers.domain import DomainList,DomainSelect,DomainUpdate,DomainAdd
# urlpatterns = [
# 	(r'/statistics',domain_statis.StatisticsList),
# 	(r'/updatedom',domain_statis.StatisticsUpdate),
# 	(r'/changedom',domain_statis.StatisticsChange),
# 	(r'/statiselect',domain_statis.StatisticsSelect),
#    (r"/bairiyisanjinhuangheruhailiu",views.RegisterHandler),
# ]


urlpatterns = [
    (r"/login",LoginHandler),
    (r"/register",RegisterHandler),
    (r"/domain/list",DomainList),
    (r"/domain/select",DomainSelect),
    (r"/domain/edit",DomainUpdate),
    (r"/domain/add",DomainAdd)
]