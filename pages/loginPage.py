from google.appengine.ext import webapp
from google.appengine.api import users

class LoginPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect("/Welcome")
        else:
            greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)

