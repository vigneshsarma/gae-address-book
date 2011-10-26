import os
import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class AddressBook(db.Model):
  """Models an Address book entry with an subscriber id, name and address,  pincode and subscribed or not."""
  subid = db.StringProperty(multiline=False)
  house_name = db.StringProperty(multiline=True)
  pin = db.StringProperty(multiline=False)
  subscribed = db.BooleanProperty()

def addressbook_key():
  """Constructs a datastore key for a Addressbook entity with addressbook_name."""
  return db.Key.from_path('addressbook','default_addressbook')

class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()

    if user:
      if user.nickname()=='poornodaya.book.trust':
        template_values={
        'name':user.nickname(),
            }
        path = os.path.join(os.path.dirname(__file__), 'html/entry.html')
        self.response.out.write(template.render(path, template_values))
      else:
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, ' + user.nickname()+' you do not have access to this site.')
    else:
      self.redirect(users.create_login_url(self.request.uri))
            
class ListAllContacts(webapp.RequestHandler):
  """
  The class that can list all contacts.
  """
  def get(self):
    contacts = db.GqlQuery("SELECT * "
                            "FROM AddressBook "
                            "WHERE ANCESTOR IS :1 "
                            "ORDER BY subid DESC",
                            addressbook_key())
    template_values={'contacts':contacts,}         
    
    self.response.headers['Content-Type'] = 'text/plain'
    for contact in contacts:
      self.response.out.write('Hello, ' + contact.house_name)              

   # path = os.path.join(os.path.dirname(__file__), 'html/all_contacts.html')
    #self.response.out.write(template.render(path, template_values))
  
  
class InsertNewSubscriber(webapp.RequestHandler):
  def post(self):
                     
    addressBook = AddressBook(parent=addressbook_key())
    addressBook.subid = self.request.get('subid')
    addressBook.house_name = self.request.get('house_name')
    addressBook.pin = self.request.get('pin')
    subscribed=self.request.get('subscribed')
    if subscribed=='on':addressBook.subscribed = True
    else:addressBook.subscribed = False
    
    template_values={'subid':self.request.get('subid'),
                     'house_name':addressBook.house_name,#.replace('\n','<br>'),
                     'pin':self.request.get('pin'),
                     'subscribed':addressBook.subscribed,
                     }
    addressBook.put()
    path = os.path.join(os.path.dirname(__file__), 'html/new_entry.html')
    self.response.out.write(template.render(path, template_values))
        

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/newsubs', InsertNewSubscriber),
                                     ('/allcontacts', ListAllContacts)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
