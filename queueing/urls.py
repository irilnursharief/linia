from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-ticket/', views.get_ticket, name='get-ticket'),
    path('pre-register/', views.pre_register, name='pre-register'),
    path('ticket/<int:pk>/status/', views.ticket_status, name='ticket-status'),
    path('ajax/load-services/', views.load_services, name='load-services'),
]