import cgi
import datetime
import urllib
import wsgiref.handlers
from google.appengine.api import mail

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import rdbms
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Volunteer(db.Model):
	userid = db.StringProperty()
	name = db.StringProperty()
	address = db.StringProperty()
	email = db.StringProperty()
	home_phone = db.StringProperty()
	cell_phone = db.StringProperty()
	emergency_contact = db.StringProperty()
	emergeny_phone = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)

class LoginPage(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.redirect("/Welcome")
		else:
			greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/"))
			self.response.out.write("<html><body>%s</body></html>" % greeting)

class Welcome(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
		self.response.out.write(greeting)
		self.response.out.write("""
<form action="/SignUp"> 
<input type='submit' value='click here to sign up'></form>

<form action="/Profile"> 
<input type='submit' value='click here to see your profile'></form>
""")

class MainPage(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		user_email = user.email()
		self.response.out.write("""
	<html> <body>
	<form action="/Post" method="post">
			<div>Name<input name="name" type="text" rows="1" /></div>
			<div>Address<input name="address" type="text" rows="1" /></div>""")
		self.response.out.write("""<div>Email<input name="email" type="text" rows="1" value=""" + user_email)
		self.response.out.write("""></div>
			<div>Home Phone<input name="home_phone" type="text" rows="1" /></div> 
			<div>Cell Phone<input name="cell_phone" type="text" rows="1" /></div> 
			<div>Emergency Contact<input name="emergency_contact" type="text" rows="1" /></div>
			<div>Emergency Contact Phone<input name="emergency_phone" type="text" rows="1" /></div> 
			<div>Do you want to be on call?<input name="On call?" type="text" rows="1" /></div> 
			<div>On call preference<input name="On call preference" type="text" rows="1" /></div>
			<div>Are you an IU student?
				<input type="radio" name="iu student" /> Yes
				<input type="radio" name="not iu student" /> No
			</div>
			<div>Are you a registered sex offender?
				<input type="radio" name="sex offender" /> Yes
				<input type="radio" name="not sex offender" /> No
			</div>
			<div><input type="submit" value="Post"></div>
          </form>
          <hr>
        </body>
      </html>
		""")
		

	
class Post(webapp.RequestHandler):
	def post(self):
		name = self.request.get("name")
		address = self.request.get('address')
		email = self.request.get('email')
		home_phone = self.request.get('home_phone')
		cell_phone = self.request.get('cell_phone')
		userid = users.get_current_user().user_id()
		vol = Volunteer(key_name=name, userid=userid, name=name, address=address, 
        email=email, home_phone=home_phone, cell_phone=cell_phone)

		vol.put()
		mail.send_mail(sender="<community_kitchen@gmail.com>",
			       to=email,
			       subject="Thank you for submitting",
			       body="""Put a message that thanks them and gives them any useful information""")
		self.response.out.write("<html><body>Thanks for submitting, ")
		self.response.out.write(cgi.escape(self.request.get('name')))
		self.response.out.write("""<p> Click <a href="http://www.monroecommunitykitchen.com/"> Here 
        </a> to go back to the community kitchen website""")
		self.response.out.write("""
<form action="/Profile">
<input type='submit' value='click here to see your profile'></form>
""")
		self.response.out.write("</body></html>")

class Profile(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		q = db.GqlQuery("SELECT * FROM Volunteer WHERE userid = :1", user.user_id())
		
		for p in q:
			self.response.out.write("Name: " + p.name)
			self.response.out.write("<p> Address: " + p.address)
			self.response.out.write("<p> Email: " + p.email)
			self.response.out.write("<p> Home Phone: " + p.home_phone)
			self.response.out.write("<p> Cell Phone: " + p.cell_phone)
		#	self.response.out.write("Name: " + p.emergency_contact)
		#	self.response.out.write("Name: " + p.emergency_phone)
	


application = webapp.WSGIApplication([
  ('/', LoginPage),
  ('/Welcome', Welcome),
  ('/SignUp', MainPage),
  ('/Post', Post),
  ('/Profile', Profile),
], debug=True)

def main():
  run_wsgi_app(application)




