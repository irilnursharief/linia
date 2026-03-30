from django.urls import path
from . import views

urlpatterns = [
    path("load-services/", views.load_services, name="load-services"),
]
