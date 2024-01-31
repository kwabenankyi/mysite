from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("solution", views.solution, name="solution"),
    path("about", views.about, name="about"),
    path("privacypolicy", views.privacypolicy, name="privacypolicy"),
    path("ads.txt", views.ads, name="ads"),
    path("contact", views.contact, name="contact")
]