from django.urls import path, include
from .views import UserViewSet, CustomAuthToken, register_user, login_user
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
]
