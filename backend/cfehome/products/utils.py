from products.models import Product, Inmate, InmateBookingNumber, JurisdictionUrl, Charge
import string

def template_context_builder(c=None):
  cntxt = {}
  context = {}
  inmate_dict = {}
  letter_dict = {}
  inmate_letter_dict = {}
  inmate_letter_list = []
  letter_list = []
  cntys = []
  counter = 0
  
  if c != None:
    inmates = Inmate.objects.filter(county=c)
    cnty = c
  else:
    inmates = Inmate.objects.all().order_by('last_name')
    cnty = "All"
    
  jurisdictions = JurisdictionUrl.objects.all().order_by('title')

  for jurisdiction in jurisdictions:
    cntys.append(jurisdiction.title)

  for county in cntys:
    inmate_dict[county] = []
    
  for an_inmate in inmates:
    try:
      inmate_dict[str(an_inmate.county)].append(an_inmate)
    except:
      pass
  

    
  
  
  letters = string.ascii_uppercase
  
  for a_letter in letters:
    letter_list.append(a_letter)
    
  for x in letter_list:
    inmate_letter_dict[x] = []
  
  for a_inmate in inmates:
    try:
      inmate_letter_dict[str(a_inmate.last_name[0])].append(a_inmate)
    except:
      pass
    
  
 
  
  
  context = {
    'county':cnty,
    'inmate_letter': inmate_letter_dict,
    'inmates':inmates,
    'counties': cntys,
    'inmate_dict': inmate_dict
  }
  
  return context

def set_value_from_url(**kwargs):
  for key in kwargs.keys():
    if key == 'county':
      inmates = Inmate.objects.filter(county=kwargs[key])
      cntxt = template_context_builder()
      cntxt['county'] = kwargs[key]
      cntxt['inmates'] = inmates
  print(cntxt['county'])
  return cntxt
  

        
  
      
