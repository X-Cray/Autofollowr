from google.appengine.ext import webapp
from appengine_utilities.sessions import Session
from common import *

class VerifyPage(webapp.RequestHandler):
	def get(self):
		auth_token = self.request.get("oauth_token")
		auth_verifier = self.request.get("oauth_verifier")
		user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)

		self.session = Session(writer="cookie")
		self.session["username"] = user_info["username"]

		user = UserInfo.get_or_insert(user_info["username"])
		user.name = user_info["name"]
		user.picture = user_info["picture"]
		user.token = user_info["token"]
		user.secret = user_info["secret"]

		if not user.follow_account:
			user.follow_account = ""
			user.needed_count = 1000

		user.save()

		self.redirect('http://autofollowr.appspot.com/')
