import os
import logging
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from common import *
from data import *

class MainPage(BasicHandler):
	def get(self):
		self.load_user()
		self.response.out.write(self.__get_index())

	def post(self):
		self.load_user()
		if self.logged_user:
			self.logged_user.follow_account = self.request.get("follow_account")
			self.logged_user.needed_count = int(self.request.get("needed_count"))
			self.logged_user.save()
		self.redirect("/")

	def __get_index(self):
		# Render page.
		html_template_values = {"logged_user": self.logged_user, "username": "username" in self.session and self.session["username"]}
		path = os.path.join(os.path.dirname(__file__), "main.html")
		return template.render(path, html_template_values)
