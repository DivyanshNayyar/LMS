from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


# url for shop
# url for buy now
# url for bank details 
# url for otp 
# url for successfull transaction

urlpatterns = [
    path('shop/',views.shop, name = 'shop'),
    # path('patient/bookAppointment/<int:pk>/<str:pk2>/<str:pk3>/',
    #      views.bookAppointment, name='bookAppointment'),
    path('shop/<int:pk>/',views.buynow, name = 'buynow'),
    path('shop/<int:pk>/bankdetails/', views.bankdetails, name = 'bankdetails'),
    path('shop/<int:pk>/bankdetails/sendotp/', views.otp, name = 'sendotp'),
    path('shop/<int:pk>/bankdetails/sendotp/enterotpb/', views.transactionbig, name = 'transactionbig'),
    path('shop/<int:pk>/bankdetails/sendotp/enterotp/', views.transactionsmall, name = 'transactionsmall'),
    
]