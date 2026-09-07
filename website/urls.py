from django.urls import path

from .views import business_detail, business_list, home, careers

urlpatterns = [
    path("", home, name="home"),
    path("businesses/", business_list, name="business_list"),
    path("businesses/<slug:slug>/", business_detail, name="business_detail"),
    path("careers/", careers, name="careers"),
]