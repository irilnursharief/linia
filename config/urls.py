from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("counter/", include("counters.urls")),
    path("ajax/", include("queueing.urls_ajax")),
    path("home/", include("queueing.urls")),
]
