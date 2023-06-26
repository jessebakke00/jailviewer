from django.db import models
import datetime

class Product(models.Model):
  title = models.CharField(max_length=200)
  content = models.TextField(blank=True, null=True)
  price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
  
  @property
  def sale_price(self):
    return "%2f" %(float(self.price) * 0.8)
  
  def get_discount(self):
    return (float(self.price) - float(self.sale_price))
      
  def __str__(self):
    return self.title
  
  
class Inmate(models.Model):
  book_id = models.CharField(unique=True, max_length=30, blank=True, null=True)
  first_name = models.CharField(max_length=30, blank=True, null=True)
  middle_name = models.CharField(max_length=30, blank=True, null=True)
  last_name = models.CharField(max_length=30, blank=True, null=True)
  race = models.CharField(max_length=1, blank=True, null=True)
  sex = models.CharField(max_length=1, blank=True, null=True)
  booking_date = models.CharField(max_length=200, blank=True, null=True)
  release_date = models.CharField(max_length=200, blank=True, null=True)
  county = models.CharField(max_length=30, blank=True, null=True)
  is_sex_offender = models.BooleanField(blank=True, null=True, default=False)
  is_in_custody = models.BooleanField(blank=True, null=True, default=True)
  was_added_when = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  
  
  def __str__(self):
    return str(self.last_name) + ', ' + str(self.first_name)
    
  def first_letter(self):
    return self.last_name[:1]
  
  @property
  def was_added_at(self):
    _original_time = self.was_added_when
    offset = datetime.timedelta(hours=7)
    adj_time = _original_time - offset
    
    return  str(adj_time.hour) + ':' + str(adj_time.minute) + ':' + str(adj_time.second) + ' - ' + str(adj_time.month) + '/' + str(adj_time.day) + '/' + str(adj_time.year)
  
    
class JurisdictionUrl(models.Model):
  title = models.CharField(max_length=100, blank=True, null=True)
  base_url = models.CharField(max_length=200)
  booking_search_url = models.CharField(max_length=200,blank=True, null=True)
  inmate_search_url = models.CharField(max_length=200,blank=True, null=True)
  
  
  def __str__(self):
    return self.title
  
class SearchUrl(models.Model):
  url = models.ForeignKey(JurisdictionUrl, on_delete=models.CASCADE)
  search_url = models.CharField(max_length=200, blank=True, null=True)
  
class InmateBookingNumber(models.Model):
  inmate = models.ForeignKey(Inmate, on_delete=models.CASCADE)
  booking_id = models.CharField(unique=True, max_length=10, blank=True, null=True)
  
  
  @property
  def book_id(self):
    return self.inmate.book_id
  
  def __str__(self):
    return str(self.book_id)
  
class Charge(models.Model):
  book_id = models.ForeignKey(InmateBookingNumber, related_name='charges', on_delete=models.CASCADE)
  charge = models.CharField(max_length=100)
  book_date = models.DateField(blank=True, null=True)

  @property
  def booking_id(self):
    return(str(self.book_id.booking_id))
  
  def get_book_id(self):
    return str(self.book_id.booking_id)
  
  def __str__(self):
    return str(self.charge)
  
# class SexOffender(models.Model):
#   inmate = models.ForeignKey(Inmate, on_delete=models.CASCADE, unique=True)
#   
#   def __str__(self):
#     return str(self.inmate.first_name) + ' ' + str(self.inmate.last_name)
