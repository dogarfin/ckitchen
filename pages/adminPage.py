from google.appengine.ext import webapp

class AdminPage(webapp.RequestHandler):
    def get(self):
        if users.is_current_user_admin():
            template_values = {'one': 1}
            path = os.path.join(os.path.dirname(__file__), 'AdminPage.html')
            self.response.out.write(template.render(path, template_values))
