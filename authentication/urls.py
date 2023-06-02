from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # path('login/', views.login, name = 'login'),
    path('get_areas_for_city/', views.get_areas_for_city, name='get_areas_for_city'),
    path('get_delivery_points_for_area/', views.get_delivery_points_for_area, name='get_delivery_points_for_area'),
    # path('register/', views.register, name = 'register'),
    path('logout/', views.logout, name = 'logout'),
    path('api/login/', views.MyTokenObtainPairView.as_view(), name = 'api_login'),
    path('api/register/', views.register_user, name = 'register_user'),
    path('api/area/',views.getAreasForCity, name = 'area_user'),
    path('api/deliveryPoint/',views.getDeliveryPointsForArea, name = 'deliverypoints_user'),
    path('api/logout/', views.logoutUser, name = 'logout_user'),
    path('api/otpless_login/', views.otpless_login, name = 'otpless_login'),
    path('api/new_user_completion/', views.new_user_completion, name = 'new_user_completion'),
    path('api/refresh_token/', views.refresh_token, name='refresh_token'),
    path('api/verify_token/', views.verify_token, name='verify_token'),
    path('api/forget_password/', views.forget_password, name='forget_password'),
]