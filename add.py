import atom
import gdata.contacts
import gdata.contacts.service
import sys
import getpass

class ContactManager:
  def __init__(self,email,password):
    self.gd_client = gdata.contacts.service.ContactsService()
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'exampleCo-exampleApp-1'
    self.gd_client.ProgrammaticLogin()
    
  def createContact(self):
    new_contact = gdata.contacts.data.ContactEntry()
    # Set the contact's name.
    new_contact.name = self.gdata.data.Name(
      given_name=self.gdata.data.GivenName(text='Elizabeth'),
      family_name=self.gdata.data.FamilyName(text='Bennet'),
      full_name=self.gdata.data.FullName(text='Elizabeth Bennet'))
      
    #set contacts postsal address.  
    new_contact.structured_postal_address.append(
      rel=self.gdata.data.WORK_REL, primary='true',
      street=self.gdata.data.Street(text='1600 Amphitheatre Pkwy'),
      city=self.gdata.data.City(text='Mountain View'),
      region=self.gdata.data.Region(text='CA'),
      postcode=self.gdata.data.PostCode(text='94043'),
      country=self.gdata.data.Country(text='United States'))
      
     # Send the contact data to the server.
    contact_entry = self.gd_client.CreateContact(new_contact)
    print "Contact's ID: %s" % contact_entry.id.text
    return contact_entry
      
  def printAllContacts(self):
    feed = self.gd_client.GetContactsFeed()

    for i, entry in enumerate(feed.entry):
      print '\n%s %s' % (i+1, entry.title.text)
      if entry.content:
        print '    %s' % (entry.content.text)
      # Display the primary email address for the contact.
      for email in entry.email:
        if email.primary and email.primary == 'true':
          print '    %s' % (email.address)
      # Show the contact groups that this contact is a member of.
      for group in entry.group_membership_info:
        print '    Member of group: %s' % (group.href)
      # Display extended properties.
      for extended_property in entry.extended_property:
        if extended_property.value:
          value = extended_property.value
        else:
          value = extended_property.GetXmlBlobString()
        print '    Extended Property - %s: %s' % (extended_property.name, value)

    
if __name__=="__main__":
  email="poornodaya.book.trust"
  print 'password for '+email+': '
  password=getpass.getpass()


  try:
    con=ContactManager(email,password)
  except gdata.service.BadAuthentication:
    print "Invalid Password"
    sys.exit(0)
  print "You are loged In"
  
  con.printAllContacts()
