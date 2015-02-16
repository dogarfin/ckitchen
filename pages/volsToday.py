from google.appengine.ext import webapp

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

