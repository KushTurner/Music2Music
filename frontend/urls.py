from django.urls import path
from . import views

appname = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('convert/', views.convert, name='convert'),
    path('reset/', views.reset, name='reset'),
]