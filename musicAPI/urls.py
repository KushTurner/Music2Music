from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('spotify-auth/', views.authSpotify),
    path('callback/', views.callback),
    path('', views.home, name=''),
]