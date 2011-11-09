import logging
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

			logging.debug("Got user info from Twitter: %s" % (response.content))

			if response.content:
				data = json.loads(response.content)
				followers_count = int(data["followers_count"])
				msg = "%s is followed by %d users. Need to be %d'th" % (user.follow_account, followers_count, user.needed_count)
				logging.info(msg)
				self.response.out.write("%s<br />" % (msg))
	
				# Should we follow destination account now?
				if followers_count == user.needed_count - 1:
					msg = "Making follow request"
					self.response.out.write("%s<br />" % (msg))
					logging.debug(msg)
					response = client.make_request(
						"http://api.twitter.com/1/friendships/create.json",
						token=user.token,
						secret=user.secret,
						additional_params={"screen_name": user.follow_account},
						method=urlfetch.POST
					)
					msg = "Response code %d: %s" % (response.status_code, response.content)
					self.response.out.write("%s<br />" % (msg))
					logging.debug(msg)
