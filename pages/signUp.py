from google.appengine.ext import webapp

class SignUp(webapp.RequestHandler):
    def get(self):
        if users.is_current_user_admin():
            user = users.get_current_user()
            user_email = user.email()
            template_values = {
                'user': user,
                'user_email': user_email,
            }                
            path = os.path.join(os.path.dirname(__file__), 'SignUp.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.response.out.write("must be an admin")
