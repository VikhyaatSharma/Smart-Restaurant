from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name='home'),
    path("signin", views.signin, name='signin'),
    path("signout",views.signout, name="signout"),
    path("status",views.status, name="status"),
    path("await",views.awaitt, name="await"),
    path("payment",views.payment, name="payment"),
    path("stattokenchange",views.stattokenchange, name="stattokenchange"),
]
