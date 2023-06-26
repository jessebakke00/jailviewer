from django.urls import path

from api import views


urlpatterns = [
  path('', views.inmate_alt_view),
  path('inmates/', views.inmate_list_view),
  path('inmates/create/', views.inmate_create_view),
  path('inmates/delete/<str:book_id>/', views.inmate_destroy_view),
  # path('inmates/change/<str:book_id>/', views.inmate_change_view),
  path('inmates/detail/<str:book_id>/', views.inmate_detail_view),
  path('charges/', views.inmate_charge_view),
  path('charges/create/', views.inmate_charge_create_view),
  path('charges/detail/<str:book_id>/', views.inmate_charges),
  path('booking_numbers/', views.booking_number_view),
  path('booking_numbers/create/', views.booking_number_create_view),
  
  
  # path('inmates/current/', views.current_inmates),
]