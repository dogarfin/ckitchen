from google.appengine.ext import webapp

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
