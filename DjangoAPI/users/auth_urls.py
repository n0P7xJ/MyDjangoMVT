from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('password-reset/', views.password_reset_request, name='password-reset'),
    path('password-reset/<uidb64>/<token>/', views.password_reset_confirm, name='password-reset-confirm'),
]
