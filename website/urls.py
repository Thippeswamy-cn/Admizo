from django.urls import path

from .views import home, careers

urlpatterns = [
    path("", home, name="home"),
    path("careers/", careers, name="careers"),
]
