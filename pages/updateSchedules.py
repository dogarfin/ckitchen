from google.appengine.ext import webapp 

#add something that chacks to make sure the schedules got updated successfully                      
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
                new_sched = p.schedule[1:]
                new_station = p.stations[1:]
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

