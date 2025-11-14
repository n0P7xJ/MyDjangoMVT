from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.base import ContentFile
import io

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            img_io = io.BytesIO()
            img.save(img_io, format='WEBP')
            self.photo.save(self.photo.name.replace('.jpg', '.webp').replace('.png', '.webp'), ContentFile(img_io.getvalue()), save=False)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
