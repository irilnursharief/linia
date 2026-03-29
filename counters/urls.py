from django.urls import path
from . import views

urlpatterns = [
    path('', views.counter_dashboard, name='counter-dashboard'),
    path('call-next/', views.call_next, name='counter-call-next'),
    path('recall/', views.recall, name='counter-recall'),
    path('no-show/', views.no_show, name='counter-no-show'),
    path('complete/', views.complete, name='counter-complete'),
]