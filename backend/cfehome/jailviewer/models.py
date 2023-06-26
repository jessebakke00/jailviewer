from django.db import models

# Create your models here.
class Inmate(models.Model):
  inmate_booking_id = models.CharField(max_length=30)
  first_name = models.CharField(max_length=50)
  middle_name = models.CharField(max_length=20)
  last_name = models.CharField(max_length=30)
  
  race = models.CharField(max_length=1, blank=True, null=True)
  sex = models.CharField(max_length=1, blank=True, null=True)