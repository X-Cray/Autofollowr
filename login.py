from google.appengine.ext import webapp
from common import *

class LoginPage(webapp.RequestHandler):
	def get(self):
		self.redirect(client.get_authorization_url())
