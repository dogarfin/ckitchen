from google.appengine.ext import db

class WorkDay(db.Model):
    day = db.DateProperty(auto_now_add=True)
    position1 = db.StringProperty()
    position2 = db.StringProperty()
    position3 = db.StringProperty()
    position4 = db.StringProperty()
    position5 = db.StringProperty()


