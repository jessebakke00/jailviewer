from rest_framework import serializers

from products.models import Product, Inmate, Charge, InmateBookingNumber

class InmateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Inmate
    fields = [
      'book_id',
      'first_name',
      'middle_name',
      'last_name',
      'race',
      'sex',
      'booking_date',
      'release_date',
      'county'
    ]
    
class ChargesSerializer(serializers.ModelSerializer):
  book_id = serializers.StringRelatedField(many=False)
  class Meta:
    model = Charge
    fields = [
      'book_id',
      
      'charge',
      'book_date'
    ]
    
class BookingNumberSerializer(serializers.ModelSerializer):
  inmate = serializers.StringRelatedField()
  charges = serializers.StringRelatedField(many=True)
  
  class Meta:
    model = InmateBookingNumber
    fields = [
      'inmate',
      'booking_id',
      'charges'
    ]