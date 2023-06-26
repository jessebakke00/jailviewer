from django.urls import path
from products import views



urlpatterns = [
  path('', views.products_home),
  path('flex/', views.flex_test, name='flex'),
  path('fetch_charges/', views.fetch_charges, name='fetch_charges'),
  path('inmates/', views.inmates, name='all_inmates'),
  path('inmates/sex_offenders/', views.sex_offenders, name='rapos'),
  path('in_custody/', views.in_custody, name='in_custody'),
  path('in_custody/<str:county>/', views.in_custody_by_county, name='custody_by_county'),
  path('inmates/<str:book_id>/', views.inmate_detail, name='inmate_detail'),
  path('inmates/county/<str:county>/', views.inmate_county, name='county'),
  path('search/by_book_id/<str:booking_id>/', views.get_charges_from_booking_number),
]
