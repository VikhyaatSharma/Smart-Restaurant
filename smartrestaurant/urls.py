from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "smartrestaurant | Admin Portal"
# admin.site.site_title = "smartrestaurant | Admin Portal"
admin.site.index_title = "smartrestaurant | Administration Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('home.urls'))
]
