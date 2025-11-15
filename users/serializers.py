from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'photo_url', 'date_joined']

    def get_photo_url(self, obj):
        profile = getattr(obj, 'profile', None)
        return profile.photo.url if profile and profile.photo else None
