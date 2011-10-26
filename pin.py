import urllib2,urllib
import sgmllib,re

class PostalPinHandler(sgmllib.SGMLParser):
  """
  Parser for pincode.net.in to get the details of the
  perticular pin.
  """
  def parse(self):
    "Parse the given string 's'."
    self.feed(self.getWebpage())
    self.close()
  
  def __init__(self,pin,verbose=0):
    sgmllib.SGMLParser.__init__(self, verbose)
    self.pin=pin
    self.pinDetails={'pin':pin}
    self.inside_a_element = 0
    self.parse()
        
  def handle_data(self, data):
    if self.inside_a_element == 0:
      mat=re.search("Post Office:",data)
      if mat:
        self.inside_a_element +=1
    elif self.inside_a_element == 1:self.inside_a_element +=1
    elif self.inside_a_element == 2:
      self.pinDetails['post_office']=data
      self.inside_a_element +=1
    if self.inside_a_element == 3:
      mat=re.search("District:",data)
      if mat:self.inside_a_element +=1
    elif self.inside_a_element == 4:self.inside_a_element +=1
    elif self.inside_a_element == 5:
      self.pinDetails['district']= data
      self.inside_a_element +=1
    if self.inside_a_element == 6:
      mat=re.search("State:",data)
      if mat:self.inside_a_element +=1
    elif self.inside_a_element == 7:self.inside_a_element +=1
    elif self.inside_a_element == 8:
      self.pinDetails['state'] = data
      self.inside_a_element +=1
    
    #print data
  
  def getWebpage(self):
    return urllib2.urlopen("http://pincode.net.in/"+self.pin).read()
    
    
if __name__=='__main__':
  post=PostalPinHandler('570001')
  print post.pinDetails
  
