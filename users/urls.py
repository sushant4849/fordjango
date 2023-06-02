from django.urls import path
from . import views
urlpatterns = [
    path('profile/', views.userprofile, name = 'userprofile'),
    path('profile_edit/', views.profile_edit, name = 'profile_edit'),
    path('api/profile-edit', views.profileEdit, name = 'profileEdit'),
    path('api/user-profile', views.userProfile, name = 'userProfile'),
    #path('api/forgot_password', views.forgot_password, name = 'forgot_password'),
]
