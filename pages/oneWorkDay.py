from google.appengine.ext import webapp


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
