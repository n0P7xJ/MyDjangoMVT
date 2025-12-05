from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, PasswordResetRequestForm, PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse 
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.conf import settings
import urllib.request
import json


def verify_turnstile(token):
    """Verify Cloudflare Turnstile token"""
    if not token or not settings.RECAPTCHA_SECRET_KEY:
        return True  # Skip verification if no token or secret configured
    
    try:
        data = json.dumps({
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': token
        }).encode('utf-8')
        
        req = urllib.request.Request(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('success', False)
    except Exception as e:
        print(f"Turnstile verification error: {e}")
        return False  # Fail secure


@login_required
def home(request):
    context = {
        'user': request.user,
        'profile': getattr(request.user, 'profile', None)
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == "POST":
        # Verify Turnstile token
        turnstile_token = request.POST.get('cf_turnstile_response', '')
        if not verify_turnstile(turnstile_token):
            messages.error(request, 'Помилка перевірки безпеки. Спробуйте ще раз.')
            return render(request, "registration/register.html", {"form": UserRegisterForm()})
        
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


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # Генеруємо токен
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Генеруємо посилання для відновлення
            reset_url = request.build_absolute_uri(
                reverse('users:password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Готуємо email
            subject = 'Відновлення пароля'
            message = render_to_string('registration/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url
            })
            
            try:
                send_mail(subject, message, 'noreply@djangomvt.com', [email], html_message=message)
                messages.success(request, 'На вашу пошту надіслано посилання для відновлення пароля.')
                return redirect('users:login')
            except Exception as e:
                messages.error(request, f'Помилка при відправці листа: {str(e)}')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'registration/password_reset_request.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Ваш пароль успішно змінено. Тепер ви можете увійти.')
                return redirect('users:login')
        else:
            form = PasswordResetForm()
        return render(request, 'registration/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Посилання для відновлення пароля невалідне або закінчилося.')
        return redirect('users:login')


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


@login_required
def home(request):
    context = {
        'user': request.user,
        'profile': getattr(request.user, 'profile', None)
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == "POST":
        # Verify Turnstile token
        turnstile_token = request.POST.get('cf_turnstile_response', '')
        if not verify_turnstile(turnstile_token):
            messages.error(request, 'Помилка перевірки безпеки. Спробуйте ще раз.')
            return render(request, "registration/register.html", {"form": UserRegisterForm()})
        
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


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # Генеруємо токен
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Генеруємо посилання для відновлення
            reset_url = request.build_absolute_uri(
                reverse('users:password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Готуємо email
            subject = 'Відновлення пароля'
            message = render_to_string('registration/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url
            })
            
            try:
                send_mail(subject, message, 'noreply@djangomvt.com', [email], html_message=message)
                messages.success(request, 'На вашу пошту надіслано посилання для відновлення пароля.')
                return redirect('users:login')
            except Exception as e:
                messages.error(request, f'Помилка при відправці листа: {str(e)}')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'registration/password_reset_request.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Ваш пароль успішно змінено. Тепер ви можете увійти.')
                return redirect('users:login')
        else:
            form = PasswordResetForm()
        return render(request, 'registration/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Посилання для відновлення пароля невалідне або закінчилося.')
        return redirect('users:login')


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
