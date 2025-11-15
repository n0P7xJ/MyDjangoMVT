from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.base import ContentFile
import io
from common.models import UniqueWebpPath

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=UniqueWebpPath(), blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            try:
                img = Image.open(self.photo.path)
                if img.format != 'WEBP':
                    img_io = io.BytesIO()
                    img.save(img_io, format='WEBP', quality=80)
                    new_filename = self.photo.name.rsplit('.', 1)[0] + '.webp'
                    self.photo.save(new_filename, ContentFile(img_io.getvalue()), save=False)
                super().save(update_fields=['photo'])
            except Exception as e:
                print(f"Error converting image: {e}")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
