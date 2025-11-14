from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from users import views as user_views 

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', user_views.register, name='register'),
]