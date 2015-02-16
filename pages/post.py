from google.appengine.ext import webapp

class Post(webapp.RequestHandler):
    def post(self):
        if users.is_current_user_admin:
            name = self.request.get("name")
            address = self.request.get('address')
            email = self.request.get('email')
            home_phone = self.request.get('home_phone')
            cell_phone = self.request.get('cell_phone')
            userid = users.get_current_user().user_id()
            vol = Volunteer(key_name=email, 
                    userid=userid, 
                    name=name, 
                    address=address, 
                    email=email, 
                    home_phone=home_phone, 
                    cell_phone=cell_phone,
                    schedule=["11-25-2012", "11-27-2012"],
                    stations=["position1", "position2"],
                    )
        # This is for testing only
        #   vol.put()
            vol1 = Volunteer(key_name="a", 
                    userid="1", 
                    name="a", 
                    address=address, 
                    email=email, 
                    home_phone=home_phone, 
                    cell_phone=cell_phone,
                    schedule=["12-01-2012", "12-03-2012"],
                    stations=["position1", "position3"],
                    group='gr1'
                    )
            vol2 = Volunteer(key_name="b", 
                    userid="2", 
                    name="b", 
                    address=address, 
                    email=email, 
                    home_phone=home_phone, 
                    cell_phone=cell_phone,
                    schedule=["12-01-2012", "12-03-2012"],
                    stations=["position2", "position1"],
                    group='gr1'
                    )
            vol3 = Volunteer(key_name="c", 
                    userid="3", 
                    name="c", 
                    address=address, 
                    email=email, 
                    home_phone=home_phone, 
                    cell_phone=cell_phone,
                    schedule=["12-01-2012", "12-03-2012"],
                    stations=["position3", "position2"],
                    group='gr2'
                    )
            vol4 = Volunteer(key_name="d", 
                    userid="4", 
                    name="d", 
                    address=address, 
                    email=email, 
                    home_phone=home_phone, 
                    cell_phone=cell_phone,
                    schedule=["12-01-2012", "12-03-2012"],
                    stations=["position4", "position5"],
                    group='gr3'
                    )
            vol2.put()
            vol3.put()
            vol4.put()
            vol1.put()
            name = cgi.escape(self.request.get('name'))
            template_values = {
                'name': name
            }
            # Here is the end of the test
            path = os.path.join(os.path.dirname(__file__), 'Post.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.response.out.write("not an admin")
