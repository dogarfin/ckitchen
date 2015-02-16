from google.appengine.ext import webapp

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
