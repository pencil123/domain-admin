#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import tornado.web
from models.auth import Auth_model

auth_modle = Auth_model()

class LoginHandler(tornado.web.RequestHandler):

	def get(self):
		#self.render('auth/login.html',err_msg='')
		self.render('auth/login.html',err_msg='')

	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		print username,password
		user_exist = auth_modle.check_login(username,password)
		if user_exist:
			self.set_secure_cookie("account",username)
			self.redirect("/")
		else:
			err_msg = 'username or password is wrong'
			self.render('auth/login.html',err_msg=err_msg)


class RegisterHandler(tornado.web.RequestHandler):

	def get(self):
		self.render('auth/register.html',err_msg=None)

	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		register_code = self.get_argument('registercode')
		if not auth_modle.register_code(register_code):
			err_msg = 'wrong register code'
			self.render('auth/register.html',err_msg=err_msg)
			return None
		print("not run it")
		result_exe = auth_modle.register(username,password)
		if result_exe:
			self.redirect("/")
			return None
		else:
			err_msg = "username is already exits"
			self.render('auth/register.html',err_msg=err_msg)
			return None