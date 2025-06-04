from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),  
    path("chat/", views.UserScreen, name="UserScreen"), 
    path("ChatData", views.ChatData, name="ChatData"),
]
