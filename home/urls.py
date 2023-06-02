
from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home, name = 'home_api'),
    path('api/', views.Home, name = 'home_api'),
]
