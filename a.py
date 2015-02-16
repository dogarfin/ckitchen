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

class VolsToday(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            day = self.request.get("day")
            if len(day) != 10 or day[2] != "-" or day[5] != "-":
                self.response.out.write("""Date must be in the correct format
                                        <form action="/AdminPage"> 
                                                        <input type='submit' value='Go back'></form>""")
            else:
                month = int(day[0:2])
                dat = int(day[3:5]) 
                year = int(day[6:10])
                d = date(year, month, dat)
                today = datetime.datetime.now() 
                if today.date() >= d:
                    self.response.out.write("true")
                    q = db.GqlQuery("SELECT * FROM WorkDay WHERE day = :1", d)
                    id_list = []
                    for p in q:
                        id_list.append(p.position1)
                        id_list.append(p.position2)
                        id_list.append(p.position3)
                        id_list.append(p.position4)
                        id_list.append(p.position5)
                    q2 = db.GqlQuery("SELECT * FROM Volunteer WHERE userid IN :1", id_list)
                    for p in q2:
                        if p.userid == id_list[0]:
                            self.response.out.write("position1: ")
                            self.response.out.write(p.name + "<br>")
                        if p.userid == id_list[1]:
                            self.response.out.write("position2: ")
                            self.response.out.write(p.name + "<br>")
                        if p.userid == id_list[2]:
                            self.response.out.write("position3: ")
                            self.response.out.write(p.name + "<br>")
                        if p.userid == id_list[3]:
                            self.response.out.write("position4: ")
                            self.response.out.write(p.name + "<br>")
                        if p.userid == id_list[4]:
                            self.response.out.write("position5: ")
                            self.response.out.write(p.name + "<br>")    
                                        
                        
                else:
                    self.response.out.write("else") 
                    q3 = db.GqlQuery("SELECT * FROM Volunteer")
                    for p in q3:
                        if day in p.schedule:
                            index = p.schedule.index(day)
                            self.response.out.write(p.name + ": ")
                            self.response.out.write(p.stations[index] + "<br>")

class Report(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            start = self.request.get("start")
            end = self.request.get("end")
            mode = self.request.get("mode")
            if len(start) != 10 or start[2] != "-" or start[5] != "-" or end[2] != "-" or end[5] != "-":
                self.response.out.write("""Date must be in the correct format
                                        <form action="/AdminPage"> 
                                                        <input type='submit' value='Go back'></form>""")
            else:
                start_month = int(start[0:2])
                start_day = int(start[3:5])
                start_year = int(start[6:10])
                s = date(start_year, start_month, start_day)

                end_month = int(end[0:2])
                end_day = int(end[3:5])
                end_year = int(end[6:10])
                e = date(end_year, end_month, end_day)

                totals = {}
                q = db.GqlQuery("SELECT * FROM WorkDay WHERE day >= :1 AND day <= :2", s, e)
                for p in q:
                    ID = p.position1
                    if ID in totals.keys():
                        totals[ID] =  totals[ID] + 1
                    else:
                        totals[ID] = 1
                    ID = p.position2
                    if ID in totals.keys():
                        totals[ID] =  totals[ID] + 2
                    else:
                        totals[ID] = 2
                    ID = p.position3
                    if ID in totals.keys():
                        totals[ID] =  totals[ID] + 3
                    else:
                        totals[ID] = 3              
                    ID = p.position4
                    if ID in totals.keys():
                        totals[ID] =  totals[ID] + 4
                    else:
                        totals[ID] = 4
                    ID = p.position5
                    if ID in totals.keys():
                        totals[ID] =  totals[ID] + 5
                    else:
                        totals[ID] = 5
                individuals = {}
                userid_list = totals.keys()
                if mode == "individual":
                    q2 = db.GqlQuery("SELECT * FROM Volunteer WHERE userid IN :1", userid_list)
                    for p in q2:
                        individuals[p.userid] = p.name
                    list_of_pairs = []
                    for elmnt in individuals:
                        list_of_pairs.append([individuals[elmnt], str(totals[elmnt])])
                    list_of_pairs.sort(lambda x, y: cmp(y[1],x[1]))
                    for pair in list_of_pairs:  
                        self.response.out.write(pair[0] + ": ")
                        self.response.out.write(pair[1] + "<br>")
                elif mode == "group":
                    group_totals = {}
                    q = db.GqlQuery("SELECT * FROM Volunteer WHERE userid IN :1", userid_list)
                    for p in q:
                        group = p.group
                        ID = p.userid
                        if group in group_totals.keys():
                            group_totals[group] = group_totals[group] + totals[ID]
                        else:
                            group_totals[group] = totals[ID]
                    list_of_pairs = []
                    for elmnt in group_totals:
                            list_of_pairs.append([elmnt, str(group_totals[elmnt])])
                    list_of_pairs.sort(lambda x, y: cmp(y[1],x[1]))
                    for pair in list_of_pairs:
                            self.response.out.write(pair[0] + ": ")
                            self.response.out.write(pair[1] + "<br>")
                else:
                    self.response.out.write("Select type of report")
                individuals = {}
                userid_list = []
                totals = {}

                    
#add something that chacks to make sure the schedules got updated successfully                      
class UpdateSchedules(webapp.RequestHandler):
    def get(self):
        today = datetime.datetime.now() 
        year = today.year
        month = today.month 
        day = today.day
        today_str = format_month(str(month)) + "-" + format_day(str(day)) + "-" + str(year)
        self.response.out.write(today_str)
        q = db.GqlQuery("SELECT * FROM Volunteer")
        for p in q:
            if p.schedule[0] == today_str:
                self.response.out.write(p.schedule)
                new_sched = p.schedule[1:]
                new_station = p.stations[1:]
                self.response.out.write(p.schedule)
                vol = Volunteer(key_name = p.name,
                        userid=p.userid, 
                        name=p.name, 
                        address=p.address, 
                        email=p.email, 
                        home_phone=p.home_phone, 
                        cell_phone=p.cell_phone,
                        schedule=new_sched,
                        stations=new_station,
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
                today = today - timedelta(hours = 5)
        year = today.year
        month = today.month 
        day = today.day
        today_str = format_month(str(month)) + "-" + format_day(str(day)) + "-" + str(year)
        q = db.GqlQuery("SELECT * FROM Volunteer")
        
        self.response.out.write(today)
        vol1, vol2, vol3, vol4, vol5 = "", "", "", "", ""
        for p in q:
            if p.schedule[0] == today_str:
                if p.stations[0] == "position1":
                    vol1 = p.userid
                if p.stations[0] == "position2":
                    vol2 = p.userid
                if p.stations[0] == "position3":
                    vol3 = p.userid
                if p.stations[0] == "position4":
                    vol4 = p.userid
                if p.stations[0] == "position5":
                    vol5 = p.userid     
        
        workday = WorkDay(
                position1 = vol1,
            position2 = vol2,
            position3 = vol3,
            position4 = vol4,
            position5 = vol5,
            )
        workday.put()
        self.response.out.write("next day generated")


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
                    schedule=["11-25-2012", "11-27-2012"],
                    stations=["position1", "position2"],
                    )

        #   vol.put()
            vol1 = Volunteer(key_name="a", 
                    userid="1", 
                    name="a", 
                    address=address, 
                    email=email, 
                    home_phone=home_phone, 
                    cell_phone=cell_phone,
                    schedule=["11-25-2012", "11-27-2012"],
                    stations=["position1", "position3"],
                    group='gr1'
                    )
            vol2 = Volunteer(key_name="b", 
                    userid="2", 
                    name="b", 
                    address=address, 
                    email=email, 
                    home_phone=home_phone, 
                    cell_phone=cell_phone,
                    schedule=["11-25-2012", "11-27-2012"],
                    stations=["position2", "position1"],
                    group='gr1'
                    )
            vol3 = Volunteer(key_name="c", 
                    userid="3", 
                    name="c", 
                    address=address, 
                    email=email, 
                    home_phone=home_phone, 
                    cell_phone=cell_phone,
                    schedule=["11-25-2012", "11-27-2012"],
                    stations=["position3", "position2"],
                    group='gr2'
                    )
            vol4 = Volunteer(key_name="d", 
                    userid="4", 
                    name="d", 
                    address=address, 
                    email=email, 
                    home_phone=home_phone, 
                    cell_phone=cell_phone,
                    schedule=["11-25-2012", "11-27-2012"],
                    stations=["position4", "position5"],
                    group='gr3'
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
  ('/UpdateSchedules', UpdateSchedules),
  ('/VolsToday', VolsToday)
 ], debug=True)

def main():
  run_wsgi_app(application)

