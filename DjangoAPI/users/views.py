from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm 
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


@login_required
def home(request):
    context = {
        'user': request.user,
        'profile': getattr(request.user, 'profile', None)
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)  
        if form.is_valid():
            user = form.save() 
            messages.success(request, f'Акаунт {user.username} створено! Тепер увійдіть.')
            return redirect('login')
        else:
            messages.error(request, 'Помилки у формі реєстрації.')
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    context = {
        'user': request.user,
        'profile': getattr(request.user, 'profile', None)
    }
    return render(request, 'registration/profile.html', context)


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Ви успішно вийшли.')
    return redirect('home')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.select_related('profile').order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key, 
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })
