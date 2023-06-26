from django.contrib import admin
from django.db.models.query import EmptyQuerySet
from products.models import Inmate, JurisdictionUrl, InmateBookingNumber, Charge
from jviewer import jail_viewer
from api.config import SEX_CRIMES, VIOLENT_CRIMES, PROPERTY_CRIMES, DRUG_CRIMES
import time
import datetime
import requests
import json

TESTIES = False

"""
------------------------------------------------------------
 Admin Actions
------------------------------------------------------------
"""

# Inmate Actions

@admin.action(description="Test Inmate Fetch")
def inmate_tester(request, modeladmin, querydict):
  name = str(querydict[0]).split(',')
  l_name = str(name[0]).strip(' ')
  f_name = str(name[1]).strip(' ')
  ch = get_charges_by_name(l_name, f_name)
  
@admin.action(description="Maintain Inmate Records")
def inmate_records_maintain(request, modeladmin, querydict):
  inmates = Inmate.objects.filter(booking_date=None)
  inmates_total = len(inmates)
  inmates.booking_date = ' '
  for inmate in inmates:
    inmate.save()
    
  i_mates = Inmate.objects.filter(release_date=None)
  i_mates_total = len(i_mates)
  i_mates.release_date = ''
  
  for i_mate in i_mates:
    i_mate.save()
    
  total = inmates_total + i_mates_total
  
  return 1

@admin.action(description="Download and store inmates!")
def get(request, modeladmin, querydict):
  
  counter = 0
  
  while True:
    if counter == 1:
      break
    
    counter += 1
    get_inmates()
    time.sleep(36)
    
@admin.action(description="Download Inmates Biatch!!")
def api_get_inmates(request, modeladmin, querydict):
  endpoint = 'http://localhost:8000/api/inmates/create/'
  jurisdiction_urls = JurisdictionUrl.objects.all()

  for url in jurisdiction_urls:
    jail_vwr = jail_viewer.JailViewer(url.base_url)
    inmates = jail_vwr.run()
    inmate_data_list = []
      
    for key in inmates.keys():      
      json = {
        'book_id':str(key),
        'first_name':inmates[key][0],
        'last_name':inmates[key][1],
        'middle_name':inmates[key][2],
        'race':inmates[key][3],
        'sex':inmates[key][4],
        'booking_date':inmates[key][5],
        'release_date':inmates[key][7],
        'county':url.title  
      }
      response = requests.post(endpoint, json=json)
      
      if response.status_code == 200:
        inmate_data_list.append(json)
      
 
# Booking Number Actions
 
@admin.action(description='Fetch and add Inmate Booking Numbers')
def get_booking_numbers(request, modeladmin, querydict):
  booking_num_helper()

@admin.action(description="Whiskey!")
def tester(request, modeladmin, querydict):
  get_charges_with_booking_number(querydict[0])

# Charges Actions

@admin.action(description="Charges Helper")      
def charges_helper(request, modeladmin, querydict):
  in_mate = Inmate.objects.all()
  endpoint = 'http://localhost:8000/api/inmates/'
  jur_urls = JurisdictionUrl.objects.all()
  inmate_strings = str()
  inmate_data = requests.get(endpoint)
  
  for i in inmate_data:
    inmate_strings = inmate_strings + i.decode()
    
  inmate_json = json.loads(inmate_strings)
  
  for inmate in inmate_json:
    county = inmate['county']
    book_id = inmate['book_id']
    
    try:
      url = JurisdictionUrl.objects.get(title=county)
      j_v = jail_viewer.JailViewer(url.base_url)
      chgs = j_v.get_charges(book_id)
      
      for key in chgs.keys():
        chg_data_set = str()
        
        if len(chgs[key]) < 1:
          url = "http://localhost:8000/api/charges/"
          data = requests.get(url)
          
          for x in data:
            chg_data_set = chg_data_set + x.decode()
            
          all_chg_data = json.loads(chg_data_set)
      time.sleep(.5)
    except: pass

@admin.action(description='Delete Duplicate Charges')
def delete_duplicate_charges(request, modeladmin, queryset):
  inmate_booking_numbers = InmateBookingNumber.objects.all()
  counter = 18333
  
  for booking_number in inmate_booking_numbers:  
    counter = get_and_delete_charges_with_booking_number(booking_number, counter=counter)
  

@admin.action(description='Fetch Inmates Charges')
def get_charges(request, modeladmin, querydict):
  fetch_charges()
    
@admin.action(description='Find Sex Offenders')
def find_sex_offenders(request, modeladmin, queryset):
  classify_offenders(SEX_CRIMES)
                 
@admin.action(description="Delete All!")
def delete_all(request, queryset, modeladmin):
  sex_offenders = SexOffender.objects.all()
  sex_offenders.delete()

@admin.action(description="Delete Sex Offender Charges")
def delete_sex_offender_charges(request, queryset, modeladmin):
  rapos = Inmate.objects.filter(is_sex_offender=True).order_by('last_name')
  for rapo in rapos:
    print(rapo.first_name, rapo.middle_name, rapo.last_name)
 
"""
------------------------------------------------------------
 Helper Functions
------------------------------------------------------------
"""

# Inmate Helpers
@admin.action(description="Fetch and Download Inmates")
def get_inmates(request, modeladmin, querydict):
  
  inmate_list = []
  jur_url = JurisdictionUrl.objects.all()
  in_custody_inmates = Inmate.objects.filter(is_in_custody=True)
  print('[Setting Inmates Status to "not in custody"]')
  for an_inmate in in_custody_inmates:
    
    an_inmate.is_in_custody = False
    an_inmate.save()
      
  for url in jur_url:
    print(url.title)
    jj = jail_viewer.JailViewer(url.base_url)
    
    
    if url.title == 'Sweetwater':
      print('[Getting Inmates From Sweetwater County]')
      try:
        inmates = jj.get_sweetwater()
        inmate_list = []
        for inmate in inmates:
          im, created = Inmate.objects.get_or_create(
            book_id=inmate['book_id'],
            first_name=inmate['first_name'],
            last_name=inmate['last_name'],
            middle_name=inmate['middle_name'],
            race='',
            sex='',
            county=url.title,
            booking_date=inmate['book_date'],
            release_date=inmate['release_date']
          )
          
          if created == True:          
            im.save()
          inmate_list.append(im)
        for inm in inmate_list:
          inm.is_in_custody = True
          inm.save()
            
          
      except:
        pass
    else:
      print('[Fetching Inmates]')
      inmates = jj.run()
      
      for key in inmates.keys():
      
        try:
          if url.title == 'Marion':
            
            i_mate, created = Inmate.objects.get_or_create(
              book_id=key,
              first_name=inmates[key][0],
              last_name=inmates[key][1]
            )
            
            if created == True:
              i_mate.middle_name=inmates[key][2]
              i_mate.race=inmates[key][4]
              i_mate.sex=inmates[key][5]
              i_mate.booking_date=inmates[key][6]
              i_mate.release_date=inmates[key][8]
              i_mate.county=url.title
              
            if i_mate.is_in_custody != True:
              i_mate.is_in_custody = True
            i_mate.save()
          else:
            i_mate, created = Inmate.objects.get_or_create(
              book_id=key,
              first_name=inmates[key][0],
              last_name=inmates[key][1]
            )
            if created == True:
              i_mate.middle_name   = inmates[key][2]
              i_mate.race          = inmates[key][3]
              i_mate.sex           = inmates[key][4]
              i_mate.booking_date  = inmates[key][5]
              i_mate.release_date  = inmates[key][7]
              i_mate.county        = url.title
              i_mate.is_in_custody = True
              
              
              inmate_list.append(i_mate)
              
            if created == False:
              i_mate.is_in_custody = True
              
              i_mate.save()
              
              if (i_mate.booking_date == '' and len(inmates[key][5]) > 0) or (i_mate.release_date == '' and len(inmates[key][7] > 0)):
                i_mate.booking_date = inmates[key][5]
                i_mate.release_date = inmates[key][7]
                
            if i_mate.is_in_custody != True:
              i_mate.is_in_custody = True
            i_mate.save()
            time.sleep(.25)  
        except:
          pass
        
  add_booking_numbers(imates=inmate_list)
  fetch_charges(in_mate=inmate_list)
  return 

# Booking Helpers

def booking_num_helper():
  inmate_list_endpoint = 'http://localhost:8000/api/inmates/'
  add_booking_number_endpoint = 'http://localhost:8000/api/booking_numbers/create/'
  inmates_data = requests.get(inmate_list_endpoint)
  
  _inmates = str()
  booking_number_list = []
  
  for data in inmates_data:
    _inmates = _inmates + data.decode()
  
  inmates_dict = json.loads(_inmates)
  

def add_booking_numbers(imates=None):
  book_number_list = []
  
  if imates == None:
    imates = Inmate.objects.all()
  print('[Adding Booking Number]')
  for inmate in imates:
    booking_id, created = InmateBookingNumber.objects.get_or_create(inmate=inmate, booking_id=inmate.book_id)
    
    if created == True:
      book_number_list.append(booking_id)
      
      booking_id.save()  
  return

# Charge Helpers

def get_charges_by_name(last_name, first_name):
  
  inmate = Inmate.objects.get(last_name=last_name, first_name=first_name)
  inmate_booking_number = InmateBookingNumber.objects.get(booking_id=inmate.book_id)
  url = JurisdictionUrl.objects.get(title=inmate.county)
  j_viewer = jail_viewer.JailViewer(url.base_url)
  charges = j_viewer.get_charges(inmate.book_id)
  
  
def get_charges_with_booking_number(book_number):
  inmate_book_number = InmateBookingNumber.objects.get(booking_id=book_number)
  inmate = Inmate.objects.get(book_id=book_number)
  charges = Charge.objects.filter(book_id=inmate_book_number.id)
  

def get_and_delete_charges_with_booking_number(booking_id, counter=None):
  
  if counter == None:
    return

  inmate_book_number = InmateBookingNumber.objects.get(pk=booking_id.id)
  
  charges = Charge.objects.filter(book_id=inmate_book_number.id)
  charge_list = []
  
  for charge in charges:
    a_charge = str(charge)[10:]
    
    if a_charge not in charge_list:
      charge_list.append(a_charge)
      
    elif a_charge in charge_list:
      counter += 1
      charge.delete()
      
  return counter

def classify_offenders(search_terms):
  inmate_booking_number = InmateBookingNumber.objects.all()
  print('[Classifying Offenders]')
  for booking_number in inmate_booking_number:
    chgs_to_check = Charge.objects.filter(book_id=booking_number).values()
    
    for ch in chgs_to_check:  
      word_list = str(ch['charge']).split(' ')
      
      for common_word in search_terms:  
        if common_word in word_list:
          i_mate = Inmate.objects.get(book_id=booking_number)

          try:
            if common_word in SEX_CRIMES:
              
              i_mate.is_sex_offender = True
              i_mate.save()
              sex_offender = SexOffender(inmate=i_mate)
              sex_offender.save()
          except:
            pass
  return

def fetch_charges(in_mate=None):
  if in_mate == None:
    in_mate = Inmate.objects.all()
  
  for imate in in_mate:
    try:
      county = imate.county
      bk_id = imate.book_id
      i_mate_book_nmbr = InmateBookingNumber.objects.get(booking_id=bk_id)
      url = JurisdictionUrl.objects.get(title=str(county))
      jv = jail_viewer.JailViewer(url.base_url)
      chgs = jv.get_charges(bk_id)
      print('[fetching charges]')
      for key in chgs.keys():
        
        for charg in chgs[key]:
          try:
            
            chg, created = Charge.objects.get_or_create(book_id=i_mate_book_nmbr, charge=charg)
            if created == True:
              chg.save()
              
          except:
            pass
            
    except:
      pass
      
  return  

def get_sex_offenders():
  classify_offenders(SEX_CRIMES)
  
# ------------------------------------------------------------
# Model Admin Classes
# ------------------------------------------------------------

class InmateAdmin(admin.ModelAdmin):
  actions = [get_inmates, api_get_inmates, inmate_tester, inmate_records_maintain]
  search_fields = ['last_name']
  
class InmateBookingNumberAdmin(admin.ModelAdmin):
  actions = [delete_duplicate_charges, get_booking_numbers, tester]
  search_fields = ['booking_id']
  
class ChargeAdmin(admin.ModelAdmin):
  actions = [get_charges, charges_helper, find_sex_offenders]
  search_fields = ['book_id__booking_id']
  

  
'''
Admin Site Registrations
'''

admin.site.register(Inmate, InmateAdmin)
admin.site.register(JurisdictionUrl)

admin.site.register(InmateBookingNumber, InmateBookingNumberAdmin)
admin.site.register(Charge, ChargeAdmin)


