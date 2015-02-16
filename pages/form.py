from google.appengine.ext import webapp

def format_month(s):
    if len(s) < 2:
        s = "0" + s
    return s
def format_day(s):
    if len(s) < 2:
        s = "0" + s
    return s
