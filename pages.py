# Still to do...
# Add a way for Vols to sign up for hours once they are already in the database
# Add a way for Vols to see and change some of their info (not as important)
# Add a way for admins to remove hours from a person if he/she leaves early or does not show
# add to / fix the vol db model
# fix signup form
# fix position names and hours that they are worth (easy)
# set up a way for schedules to be updated and new days to be created automatically
# make it so that no one can enter any part of the site unless they are in the database

import os
import datetime
from datetime import date
from datetime import timedelta
from google.appengine.ext.webapp import template
import cgi
import datetime
import urllib
import wsgiref.handlers
import calendar

from pages.workday import WorkDay
from pages.adminPage import AdminPage
from pages.form import format_month 
from pages.form import format_day
from pages.loginPage import LoginPage
from pages.profile import Profile
from pages.signUp import SignUp
from pages.welcome import Welcome
from pages.calendar import Calendar 
# from pages.selectCal import SelectCal
from pages.oneWorkDay import OneWorkDay
from pages.report import Report
from pages.updateSchedules import UpdateSchedules
from pages.confirmation import Confirmation
from pages.post import Post 
from pages.volsToday import VolsToday

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
  ('/UpdateSchedules', UpdateSchedules),
  ('/VolsToday', VolsToday),
  ('/SelectCal', SelectCal),
  ('/Confirmation', Confirmation),
 ], debug=True)

def main():
  run_wsgi_app(application)

