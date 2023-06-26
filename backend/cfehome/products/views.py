from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from products.models import Product, Inmate, InmateBookingNumber, JurisdictionUrl, Charge
from products import utils

from jviewer import jail_viewer
import string, json


def products_home(request):
  return redirect('/products/inmates/')

def flex_test(request):
  # inmates = Inmate.objects.all().order_by('last_name')
  # 
  # jurisdictions = JurisdictionUrl.objects.all()
  # 
  # cntys = []
  # 
  # for jurisdiction in jurisdictions:
  #   cntys.append(jurisdiction.title)
  # 
  # inmate_dict = {}
  # letter_dict = {}
  # inmate_letter_dict = {}
  # 
  # inmate_letter_list = []
  # letter_list = []
  # 
  # counter = 0
  # 
  # letters = string.ascii_uppercase
  # 
  # for a_letter in letters:
  #   letter_list.append(a_letter)
  #   
  # for x in letter_list:
  #   inmate_letter_dict[x] = []
  # 
  # for a_inmate in inmates:
  #   try:
  #     inmate_letter_dict[str(a_inmate.last_name[0])].append(a_inmate)
  #   except:
  #     pass
  #     
  # for county in cntys:
  #   inmate_dict[county] = []
  # 
  # for an_inmate in inmates:
  #   try:
  #     inmate_dict[str(an_inmate.county)].append(an_inmate)
  #   except:
  #     pass
  #     
  # context = {
  #   'inmate_letter': inmate_letter_dict,
  #   'inmates':inmates,
  #   'counties': cntys,
  #   'inmate_dict': inmate_dict
  # }
  
  context = utils.template_context_builder()
  
  return render(request, 'products/flex.html', context)
 
def get_charges_from_booking_number(request, booking_id):
  inmate = Inmate.objects.get(book_id=booking_id)
  inmate_booking_number = InmateBookingNumber.objects.get(booking_id=booking_id)
  url = JurisdictionUrl.objects.get(title=inmate.county)
  search_url = str(url.base_url) + str(url.booking_search_url)
  jailvwer = jail_viewer.JailViewer(url.base_url)

  charges = jailvwer.get_charges(booking_id)

  context = {'charges':charges}
  return render(request, 'products/search_by_booking_id.html', context)

  
def inmates(request):

  context = utils.template_context_builder()
  
  # xcontext = {
  #   'inmate_letter': inmate_letter_dict,
  #   'inmates':inmates,
  #   'counties': cntys,
  #   'inmate_dict': inmate_dict
  # }
  
  return render(request, 'products/flex.html', context)

def inmate_county(request, county):
  inmate_letter_dict = {}
  letter_list = []
  counties =[]
  
  letters = string.ascii_uppercase
  for letter in letters:
    letter_list.append(letter)
    
  for x in letter_list:
    inmate_letter_dict[x] = []
  
  co = JurisdictionUrl.objects.all().order_by('title')
  for c in co:
    counties.append(c.title)
  inmates = Inmate.objects.filter(county=county).order_by('last_name')
  
  for a_inmate in inmates:
    inmate_letter_dict[a_inmate.last_name[0]].append(a_inmate)
  
  
  context = {
    'user': str(request.user),
    'inmate_letter':inmate_letter_dict,
    'county': county,
    'counties':counties,
  }
  
  

  return render(request, 'products/inmates_county.html', context)
 
def in_custody_by_county(request, county):
  i_mates = Inmate.objects.filter(county=county).exclude(is_in_custody=False)
  number_in_custody = i_mates.count()
  counties = JurisdictionUrl.objects.all().order_by('title')
  letters = string.ascii_uppercase
  letter_list = []
  inmate_letter_dict = {}
  for letter in letters:
    letter_list.append(letter)
  
  for x in letter_list:
    inmate_letter_dict[x] = []
    
  for a_inmate in i_mates:
    inmate_letter_dict[a_inmate.last_name[0]].append(a_inmate)
  
  
  context = {
    'inmate_letter':inmate_letter_dict,
    'number_in_custody':number_in_custody,
    'inmates':i_mates,
    'user'   :str(request.user),
    'cnty' :county,
    'counties':counties
  }
  
  return render(request, 'products/inmates_in_custody_county.html', context)

def fetch_charges(request):
  post_data = json.loads(request.body.decode())
  print(post_data)
  charge_list = ""
  p_data = str({"post_data":post_data})
  inmate = Inmate.objects.get(book_id=post_data['book_id'])
  book_id = InmateBookingNumber.objects.get(booking_id=post_data['book_id'])
  charges = Charge.objects.filter(book_id__id=book_id.id)
  for charge in charges.values():
    charge_list = charge_list + ';' + str(charge['charge'])
  response_dict = {}
  
  response_dict['inmate'] = {
    'first_name': inmate.first_name,
    'middle_name':inmate.middle_name,
    'last_name':inmate.last_name,
    'book_id':inmate.book_id,
    'booking_date':inmate.booking_date,
    'county':inmate.county,
    'charges':charge_list
  }
  resp_data = json.dumps(response_dict)
  # return JsonResponse(str(charge_list), safe=False)
  print(type(resp_data))
  return JsonResponse(response_dict, safe=False)
 
def inmate_detail(request, book_id):
  book_num = InmateBookingNumber.objects.get(booking_id=book_id)
  charges = Charge.objects.filter(book_id=book_num)

  oregon_revised = []
  oreg_rev = []
  for ch in charges:
    oregon_revised.append({'ors':str(ch)[0:7], 'full':str(ch)})
  
  context = {
    'user': str(request.user),
    'ore_rev':oregon_revised,
    'book_id':book_num,
    'charges':charges,
  }
  
  return render(request, 'products/inmate_detail.html', context)
  
  
def sex_offenders(request):
  sex_offenders = SexOffender.objects.all()
  counties = JurisdictionUrl.objects.all().order_by('title')
  
  context = {
    'user': str(request.user),
    'sex_offenders': sex_offenders,
    'counties': counties
  }
  
  return render(request, 'products/sex_offenders.html', context)

def in_custody(request):
  inmates = Inmate.objects.filter(is_in_custody=True).order_by('last_name')
  counties = JurisdictionUrl.objects.all().order_by('title')
  letters = string.ascii_uppercase
  inmate_letter_dict = {}
  letter_list = []
  for letter in letters:
    letter_list.append(letter)
    
  for x in letter_list:
    inmate_letter_dict[x] = []
    
  for inmate in inmates:
    inmate_letter_dict[inmate.last_name[0]].append(inmate)
    
  context = {
    'inmate_letter': inmate_letter_dict,
    'inmates'     : inmates,
    'letter_list' : letter_list,
    'user'        : str(request.user),
    'counties': counties,
  }

  return render(request, 'products/in_custody.html', context)
