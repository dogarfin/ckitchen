import os
import datetime
from datetime import date
from google.appengine.ext.webapp import template
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
	schedule = db.StringListProperty()
	stations = db.StringListProperty()
	group = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	
class WorkDay(db.Model):
	day = db.DateProperty(auto_now_add=True)
	position1 = db.StringProperty()
	position2 = db.StringProperty()
	position3 = db.StringProperty()
	position4 = db.StringProperty()
	position5 = db.StringProperty()

class AdminPage(webapp.RequestHandler):
	def get(self):
		if users.is_current_user_admin():
			template_values = {'one': 1}
			path = os.path.join(os.path.dirname(__file__), 'AdminPage.html')
			self.response.out.write(template.render(path, template_values))

class Report(webapp.RequestHandler):
	def post(self):
		if users.is_current_user_admin():
			start = self.request.get("start")
			end = self.request.get("end")
			if len(start) < 10 or len(end) < 10:
				start = "          "
				end = "          "
			if start[2] != "-" or start[5] != "-" or end[2] != "-" or end[5] != "-":
				self.response.out.write("""Date must be in the correct format
				                        <form action="/AdminPage"> 
                                                        <input type='submit' value='Go back'></form>""")
			
			
			start_month = int(start[0:2])
			start_day = int(start[3:5])
			start_year = int(start[6:10])
			s = date(start_year, start_month, start_day)
			
			end_month = int(end[0:2])
			end_day = int(end[3:5])
			end_year = int(end[6:10])
			e = date(end_year, end_month, end_day)
			
			totals = {}
			q = db.GqlQuery("SELECT * FROM WorkDay WHERE date >= :1 AND date <= :2", s, e)
							
			for p in q:
		      	       	name = p.position1
				if name in totals.keys():
					totals[name] =  totals[name] + 4
				else:
					totals[name] = 4
				name = p.position2
				if name in totals.keys():
					totals[name] =  totals[name] + 4
				else:
					totals[name] = 4
				name = p.position3
				if name in totals.keys():
					totals[name] =  totals[name] + 4
				else:
					totals[name] = 4				
				name = p.position4
				if name in totals.keys():
					totals[name] =  totals[name] + 4
				else:
					totals[name] = 4
				name = p.position5
				if name in totals.keys():
					totals[name] =  totals[name] + 4
				else:
					totals[name] = 4
		 	self.response.out.write(totals.keys())
		 	self.response.out.write(totals.values())
				
#A class called UpdateSchedules will shorten Vols schedules at the end of a day. There should be a check to make sure
#the data from the schedule lists successfully made it into the WorkDay database
class UpdateSchedules(webapp.RequestHandler):
	def get(self):
		today = datetime.datetime.now()
		year = today.year
		month = today.month 
		day = today.day
		today_str = format_month(str(month)) + "-" + format_day(str(day)) + "-" + str(year)
		q = db.GqlQuery("SELECT * FROM Volunteer")
		for p in q:
			if p.schedule[0] == today_str:
				del p.schedule[0]
				del p.stations[0]
			vol = Volunteer(key_name = p.email,
					userid=p.userid, 
					name=p.name, 
					address=p.address, 
					email=p.email, 
					home_phone=p.home_phone, 
					cell_phone=p.cell_phone,
					schedule=[""],
					stations=[""],
					)
			vol.put()

def format_month(s):
	if len(s) < 2:
		s = "0" + s
	return s
def format_day(s):
	if len(s) < 2:
		s = "0" + s
	return s
			
class OneWorkDay(webapp.RequestHandler):
	def get(self):
		today = datetime.datetime.now()
		year = today.year
		month = today.month 
		day = today.day
		today_str = format_month(str(month)) + "-" + format_day(str(day)) + "-" + str(year)
		q = db.GqlQuery("SELECT * FROM Volunteer")
		
		self.response.out.write(today_str)
		vol1, vol2, vol3, vol4, vol5 = "", "", "", "", ""
		for p in q:
			if p.schedule[0] == today_str:
				if p.stations[0] == "position1":
					vol1 = p.name
				if p.stations[0] == "position2":
					vol2 = p.name
				if p.stations[0] == "position3":
					vol3 = p.name
				if p.stations[0] == "position4":
					vol4 = p.name
				if p.stations[0] == "position5":
					vol5 = p.name		
		
		workday = WorkDay(
		      	position1 = vol1,
			position2 = vol2,
			position3 = vol3,
			position4 = vol4,
			position5 = vol5,
			)
		workday.put()
		self.response.out.write("hello")


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
                nickname = user.nickname()
                logout_url = users.create_logout_url("/")
                template_values = {
                    'user': user,
                    'nickname': nickname,
                    'logout_url': logout_url
                }
	#	if users.is_current_user_admin():
	#		path = os.path.join(os.path.dirname(__file__), 'AdminPage.html')
	#		self.response.out.write(template.render(path, template_values))
	#	else:
       		path = os.path.join(os.path.dirname(__file__), 'Welcome.html')
       		self.response.out.write(template.render(path, template_values))

class SignUp(webapp.RequestHandler):
	def get(self):
		if users.is_current_user_admin():
			user = users.get_current_user()
			user_email = user.email()
			template_values = {
			    'user': user,
			    'user_email': user_email,
			}                
			path = os.path.join(os.path.dirname(__file__), 'SignUp.html')
			self.response.out.write(template.render(path, template_values))
		else:
			self.response.out.write("must be an admin")

class Post(webapp.RequestHandler):
	def post(self):
		if users.is_current_user_admin:
			name = self.request.get("name")
			address = self.request.get('address')
			email = self.request.get('email')
			home_phone = self.request.get('home_phone')
			cell_phone = self.request.get('cell_phone')
			userid = users.get_current_user().user_id()
			vol = Volunteer(key_name=email, 
					userid=userid, 
					name=name, 
					address=address, 
					email=email, 
					home_phone=home_phone, 
					cell_phone=cell_phone,
					schedule=["11-10-2012"],
					stations=["position1"],
					)

			vol.put()
			vol1 = Volunteer(key_name="a", 
					userid="1", 
					name="a", 
					address=address, 
					email=email, 
					home_phone=home_phone, 
					cell_phone=cell_phone,
					schedule=["11-10-2012"],
					stations=["position2"],
					)
			vol2 = Volunteer(key_name="b", 
					userid="2", 
					name="b", 
					address=address, 
					email=email, 
					home_phone=home_phone, 
					cell_phone=cell_phone,
					schedule=["11-10-2012"],
					stations=["position3"],
					)
			vol3 = Volunteer(key_name="c", 
					userid="3", 
					name="c", 
					address=address, 
					email=email, 
					home_phone=home_phone, 
					cell_phone=cell_phone,
					schedule=["11-10-2012"],
					stations=["position4"],
					)
			vol4 = Volunteer(key_name="d", 
					userid="d", 
					name=name, 
					address=address, 
					email=email, 
					home_phone=home_phone, 
					cell_phone=cell_phone,
					schedule=["11-10-2012"],
					stations=["position5"],
					)
			vol2.put()
			vol3.put()
			vol4.put()
			vol1.put()
			name = cgi.escape(self.request.get('name'))
			template_values = {
			    'name': name
			}
			path = os.path.join(os.path.dirname(__file__), 'Post.html')
			self.response.out.write(template.render(path, template_values))
		else:
			self.response.out.write("not an admin")

class Profile(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		q = db.GqlQuery("SELECT * FROM Volunteer WHERE userid = :1", user.user_id())
		template_values = {
			'q': q,
			'user': user
		}
		path = os.path.join(os.path.dirname(__file__), 'Profile.html')
		self.response.out.write(template.render(path, template_values))
		
class Calendar(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		now = datetime.datetime.now()
		month = now.month
		year = now.year
		firstday = db.GqlQuery("SELECT * FROM WorkDay WHERE d = 1 AND month = :1 AND year = :2", month, year)
		
		day1 = 0
		for f in firstday:
			day1 = f.day
		
		if day1 == 6:
			day1 = 0
		else:
			day1 += 1
		
		next_month = month + 1
		previous_month = month - 1
		if (next_month == 13):
			next_month = 1
		if (previous_month == 0):
			previous_month = 12

		total_days =  (date(year, next_month, 1) - date(year, month, 1)).days
		total_previous =  (date(year, month, 1) - date(year, previous_month, 1)).days
		dates = []
		i = 0
		d = 1
		over = 1
		while (i < 34):
			if (i < day1):
				dates.append(total_previous - (day1-i))
			elif (d > total_days):
				dates.append(over)
				over += 1
			else:
				dates.append(d)
				d += 1
			i += 1
				

		schedule = db.GqlQuery("SELECT * FROM WorkDay WHERE month = :1 AND year = :2", month, year)

		template_values = {
			'schedule': schedule,
			'user': user,
			'dates': dates,
			}
      
		path = os.path.join(os.path.dirname(__file__), 'Calendar.html')
		self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication([
  ('/', LoginPage),
  ('/Welcome', Welcome),
  ('/SignUp', SignUp),
  ('/Post', Post),
  ('/Profile', Profile),
  ('/Calendar', Calendar),
   ('/AdminPage', AdminPage),
  ('/OneWorkDay', OneWorkDay),
  ('/Report', Report),
  ('/UpdateSchedules', UpdateSchedules)
], debug=True)

def main():
  run_wsgi_app(application)

