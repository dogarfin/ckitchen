from google.appengine.ext import webapp

class Welcome(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        nickname = user.nickname()
        logout_url = users.create_logout_url("/")
        template_values = {
                    'user': user,
                    'nickname': nickname,
                    'logout_url': logout_url
                    }
        path = os.path.join(os.path.dirname(__file__), 'Welcome.html')
        self.response.out.write(template.render(path, template_values))

