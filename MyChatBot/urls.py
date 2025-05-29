from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserScreen, name="UserScreen"),  # Make this the default route
    path("ChatData", views.ChatData, name="ChatData"),
]
