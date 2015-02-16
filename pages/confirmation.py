from google.appengine.ext import webapp

class Confirmation(webapp.RequestHandler):
    def post(self):
        self.response.out.write("hello")

