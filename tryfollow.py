from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from django.utils import simplejson as json
from common import *

class TryFollowPage(webapp.RequestHandler):
	def get(self):
		all_users = UserInfo.all()

		for user in all_users:
			response = client.make_request(
				"http://api.twitter.com/1/users/show.json",
				token=user.token,
				secret=user.secret,
				additional_params={"screen_name": user.follow_account},
				method=urlfetch.GET
			)

			data = json.loads(response.content)
			followers_count = int(data["followers_count"])
			self.response.out.write("%s is following %d users. Need to be %d'th<br />" % (user.follow_account, followers_count, user.needed_count))

			# Should we follow destination account now?
			if followers_count == user.needed_count - 1:
				self.response.out.write("Making follow request<br />")
				response = client.make_request(
					"http://api.twitter.com/1/friendships/create.json",
					token=user.token,
					secret=user.secret,
					additional_params={"screen_name": user.follow_account},
					method=urlfetch.POST
				)
				self.response.out.write("Response code %d: %s" % (response.status_code, response.content))
