from django.urls import path
from . import views

urlpatterns = [
    path("analyser", views.sent_anal, name="analyser"),
    path("login", views.login, name="login"),
]