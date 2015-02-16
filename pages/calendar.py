from google.appengine.ext import webapp

class Calendar(webapp.RequestHandler):
    def post(self):
         user = users.get_current_user()
         current_month = int(self.request.get("month"))
         current_year = int(self.request.get("year"))
         mrange = calendar.monthrange(current_year, current_month)
         first_day = mrange[0]
         if first_day == 6:
             first_day = 0
         else:
             first_day += 1
         
         total_days = mrange[1]
        
         pos1 = []
         pos2 = []
         pos3 = []
         pos4 = []
         pos5 = []

         while len(pos1) < first_day:
             pos1.append("")
             pos2.append("")
             pos3.append("")
             pos4.append("")
             pos5.append("")

         while len(pos1) < total_days + first_day:
             pos1.append("position1")
             pos2.append("position2")
             pos3.append("position3")
             pos4.append("position4")
             pos5.append("position5")

         while len(pos1) < 42:
             pos1.append("")
             pos2.append("")
             pos3.append("")
             pos4.append("")
             pos5.append("")


         q = db.GqlQuery("SELECT * FROM Volunteer")

         dates = []
         d = 0
         while d < first_day:
             dates.append("")
             d += 1
         d = 1
         while d <= total_days:
             dates.append(d)
             if d < 10:
                 date_string = str(current_month) + "-0" + str(d) + "-" + str(current_year)
             else:
                 date_string = str(current_month) + "-" + str(d) + "-" + str(current_year)
             for p in q:
                 if date_string in p.schedule:
                     stat = p.stations[p.schedule.index(date_string)]
                     if stat == "position1":
                         pos1[first_day+d-1] = ""
                     elif stat == "position2":
                         pos2[first_day+d-1] = ""
                     elif stat == "position3":
                         pos3[first_day+d-1] = ""
                     elif stat == "position4":
                         pos4[first_day+d-1] = ""
                     elif stat == "position5":
                         pos5[first_day+d-1] =""
             d += 1
         while len(dates) < 42:
            dates.append("")

         template_values = {
             "current_month": current_month,
             "current_year": current_year,
             "first_day": first_day,
             "total_days": total_days,
             "dates": dates,
             "pos1": pos1,
             "pos2": pos2,
             "pos3": pos3,
             "pos4": pos4,
             "pos5": pos5,
             }
      
         path = os.path.join(os.path.dirname(__file__), 'Cal.html')
         self.response.out.write(template.render(path, template_values))




