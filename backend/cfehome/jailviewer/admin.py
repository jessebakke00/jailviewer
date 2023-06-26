from django.contrib import admin


import os, sys
from bs4 import BeautifulSoup

# import base64
import string
# import re
import time
# import urllib, urllib3
import requests
from .models import Inmate    
  
class JailViewer(object):
  def __init__(self):
    pass
        
  def _build_url(self):
    url_list = []
    for letter in string.ascii_lowercase:
      url_list.append('http://jailviewer.co.douglas.or.us/Home/BookingSearchResult?LastName=' + str(letter) + '%&FirstName=&BookingFrom=&BookingTo=&ReleaseFrom=&ReleaseTo=&Status=IN+CUSTODY')
    return url_list
    
  def fetch(self, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    trs = soup.find_all("td", class_='text-success')
    
    counter = 0
    inmate_details = []
    inmate_dict = {}

    for tr in trs:
      sibs = tr.find_next_siblings("td")
      for inm in sibs:
        inmate_details.append(str(inm).strip('<>td/'))
      inmate_dict[inmate_details[0]] = inmate_details[1:6]
      inmate_details = []
      
    for key in inmate_dict.keys():
      inmate = models.Inmate(
        inmate_id   =key,
        first_name  =inmate_dict[key][0],
        middle_name =inmate_dict[key][1],
        last_name   =inmate_dict[key][2],
        dob         ='',
        race        =inmate_dict[key][3],
        sex         =inmate_dict[key][4],
        )
      inmate.save()
      
      print(key, ' ', inmate_dict[key])

    time.sleep(1)

  def run(self):
    url_list = self._build_url()
    for url in url_list:
      
      
      self.fetch(url)
    print(len(url_list))
    
@admin.action(description="Download and save current inmates")
def get_inmates(modeladmin, request, queryset):
  jailviewer = JailViewer()
  jailviewer.run()
  
class InmateAdmin(admin.ModelAdmin):
  actions = ['get_inmates']
  
admin.site.register(Inmate, InmateAdmin)
      

      
