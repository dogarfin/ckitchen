from google.appengine.ext import webapp

class SelectCal(webapp.RequestHandler):
    def get(self):
        template_values = {'one': 1}
        path = os.path.join(os.path.dirname(__file__), 'SelectCal.html')
        self.response.out.write(template.render(path, template_values))
