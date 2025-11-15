from django.urls import path, include
from . import views
from .views import UserViewSet
from django.contrib.auth.views import LoginView, LogoutView
from users import views as user_views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', user_views.register, name='register'),
]