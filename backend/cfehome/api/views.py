from django.forms.models import model_to_dict

from jviewer import jail_viewer

from rest_framework import authentication, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins, permissions
from rest_framework import permissions, authentication
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from products.serializers import InmateSerializer, ChargesSerializer, BookingNumberSerializer
# from products.permissions import IsStaffEditorPermission
from products.models import Inmate, Charge, JurisdictionUrl, InmateBookingNumber

@api_view(["GET"])
def inmate_charges(request, book_id=None, *args, **kwargs):
  book_num = InmateBookingNumber.objects.get(booking_id=book_id)
  charges = Charge.objects.filter(book_id=book_num)
  data = ChargesSerializer(charges, many=True).data
  return Response(data)

  

@api_view(["POST"])
def api_home(request, *args, **kwargs):
  serializer = InmateSerializer(data=request.data)
  if serializer.is_valid():
    instance = serializer.save()
    print(instance)
    data = serializer.data
    return Response(data)
 
@api_view(['GET', 'POST'])
def inmate_alt_view(request, book_id=None, *args, **kwargs):
  method = request.method
  
  if method == 'GET':
    if book_id is not None:
      obj = get_object_or_404(Inmate, book_id=book_id)
      data = InmateSerializer(obj, many=False).data
      return Response(data)
      
    
    queryset = Inmate.objects.all()
    data = InmateSerializer(queryset, many=True).data
    return Response(data)
    
  
  if method == 'POST':
    serializer = InmateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      book_id = serializer.validated_data.get('book_id')
      first_name = serializer.validated_data.get('first_name')
      middle_name = serializer.validated_data.get('middle_name')
      last_name = serializer.validated_data.get('last_name')
      race = serializer.validated_data.get('race')
      sex = serializer.validated_data.get('sex')
      booking_date = serializer.validated_data.get('booking_date')
      release_date = serializer.validated_data.get('release_date')
      serializer.save(
        book_id=book_id,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        race=race,
        sex=sex,
        booking_date=booking_date,
        release_date=release_date
      )
    
      print(serializer.data)
      return Response(serializer.data)
    return Response({'invalid':'not good data'}, status=400)
 
@api_view(['POST'])
def create_inmate(request):
  method = request.method
  if method == 'POST':
    serializer = InmateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      print(serializer.data)
      return Response(serializer.data)
    return Response({"invalid":"not good data"}, status=400)

# class InmateMixinAPIView(
#   mixins.CreateModelMixin,
#   mixins.ListModelMixin,
#   mixins.RetrieveModelMixin,
#   generics.GenericAPIView,
#   ):
#   queryset = Inmate.objects.all()
#   serializer_class = InmateSerializer
#   lookup_field = 'book_id'
#   
#   
#   
#   def get(self, request, *args, **kwargs):
#     book_id = kwargs.get('book_id')
#     if book_id is not None:
#       return self.retrieve(request, *args, **kwargs)
#     return self.list(request, *args, **kwargs)
#   
#   def post(self, request, *args, **kwargs):
#     return self.create(request, *args, **kwargs)
#   
#   def perform_create(self, serializer):
    
    
  
class InmateListAPIView(generics.ListAPIView):
  queryset = Inmate.objects.all()
  serializer_class = InmateSerializer
  # authentication_classes = [authentication.SessionAuthentication]
  # permission_classes = [IsStaffEditorPermission]
  
class InmateDetailAPIView(generics.RetrieveAPIView):
  queryset = Inmate.objects.all()
  serializer_class = InmateSerializer
  
class InmateCreateAPIView(generics.CreateAPIView):
  queryset = Inmate.objects.all()
  serializer_class = InmateSerializer
  # permission_classes = [permissions.IsAuthenticated]
  
  def perform_create(self, serializer):
    
    serializer.save()
    

class InmateDestroyAPIView(generics.DestroyAPIView):
  
  queryset = Inmate.objects.all()
  serializer_class = InmateSerializer
  # authentication_classes = [authentication.SessionAuthentication]
  # permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
  lookup_field = 'book_id'
  
  def delete(self, request, *args, **kwargs):
    return self.perform_delete(instance)
  
  # def perform_destroy(self, instance):
  #   super().perform_destroy(instance)
  

class ChargeListAPIView(generics.ListAPIView):
  queryset = Charge.objects.all()
  serializer_class = ChargesSerializer
  
class ChargeCreateAPIView(generics.CreateAPIView):
  queryset = Charge.objects.all()
  serializer_class = ChargesSerializer
  
  def perform_create(self, serializer):
    serializer.save()
  
class BookingNumberListAPIView(generics.ListAPIView):
  
  queryset = InmateBookingNumber.objects.all()
  serializer_class = BookingNumberSerializer

class BookingNumberCreateAPIView(generics.CreateAPIView):
  queryset = InmateBookingNumber.objects.all()
  serializer_class = BookingNumberSerializer
  
  def perform_create(self, serializer):
    serializer.save()

inmate_create_view = InmateCreateAPIView.as_view()
inmate_detail_view = InmateDetailAPIView.as_view()  
inmate_list_view = InmateListAPIView.as_view()
inmate_destroy_view = InmateDestroyAPIView.as_view()
inmate_charge_view = ChargeListAPIView.as_view()
inmate_charge_create_view = ChargeCreateAPIView.as_view()
booking_number_view = BookingNumberListAPIView.as_view()
booking_number_create_view = BookingNumberCreateAPIView.as_view()