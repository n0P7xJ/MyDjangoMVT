from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from .models import Profile
from PIL import Image
import io

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    photo = forms.ImageField(required=False, label="Фото профілю")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3 col-form-label'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Field('username', css_class='form-control', placeholder='Ім\'я користувача'),
            Field('email', css_class='form-control', placeholder='Email'),
            Field('password1', css_class='form-control', placeholder='Пароль'),
            Field('password2', css_class='form-control', placeholder='Підтвердіть пароль'),
            Field('photo', css_class='form-control', css_id='photo-input'),
            Submit('submit', 'Зареєструватися', css_class='btn btn-primary btn-lg btn-block')
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            if self.cleaned_data.get('photo'):
                photo = self.cleaned_data['photo']
                try:
                    img = Image.open(photo)
                    if img.format != 'WEBP':
                        img_io = io.BytesIO()
                        img.save(img_io, format='WEBP', quality=85)
                        cropped_filename = f"{photo.name.rsplit('.', 1)[0]}.webp"
                        profile.photo.save(cropped_filename, img_io, save=False)
                    else:
                        profile.photo = photo
                    profile.save()
                except Exception as e:
                    print(f"Error processing photo: {e}")
        return user


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True, label='Email адреса')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Користувач з такою email адресою не знайдений.')
        return email


class PasswordResetForm(forms.Form):
    new_password1 = forms.CharField(
        label='Новий пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть новий пароль'})
    )
    new_password2 = forms.CharField(
        label='Підтвердіть пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторіть пароль'})
    )
    
    def clean(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Паролі не збігаються.')
            if len(password1) < 8:
                raise forms.ValidationError('Пароль має бути не менше 8 символів.')
        return self.cleaned_data
