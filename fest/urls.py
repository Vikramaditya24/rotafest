from django.contrib import admin
from django.urls import path
from fest import views
urlpatterns = [
    path('', views.index,name='index'),
    path('pay/<str:event>,<str:fee>', views.payform,name='payform'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]
