from google.appengine.ext import db

class UserInfo(db.Model):
	name = db.StringProperty()
	picture = db.StringProperty()
	token = db.StringProperty()
	secret = db.StringProperty()
	follow_account = db.StringProperty()
	needed_count = db.IntegerProperty()
