from django.urls import path
from . import views

app_name = "display"

urlpatterns = [
    path("<int:branch_id>/", views.display_main, name="display_main"),
    path("<int:branch_id>/update/", views.display_update, name="display_update"),
]
