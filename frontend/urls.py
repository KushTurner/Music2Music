from django.urls import path
from . import views

appname = "frontend"

urlpatterns = [
    path('', views.home, name='')
]