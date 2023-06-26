"""cfehome URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from products import views

urlpatterns = [
    path('', views.products_home),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('products/', include('products.urls')),
]
