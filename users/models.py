from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.base import ContentFile
import io
from common.models import UniqueWebpPath  # Для динамічної папки

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=UniqueWebpPath(), blank=True, null=True)  # Динамічний шлях

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Спочатку зберігаємо базові дані
        if self.photo:
            try:
                img = Image.open(self.photo.path)
                if img.format != 'WEBP':  # Конвертуємо тільки якщо не WebP
                    img_io = io.BytesIO()
                    img.save(img_io, format='WEBP', quality=80)  # Якість для оптимізації
                    # Отримуємо нове ім'я з UniqueWebpPath
                    new_filename = self.photo.name.rsplit('.', 1)[0] + '.webp'
                    self.photo.save(new_filename, ContentFile(img_io.getvalue()), save=False)
                    self.photo.close()  # Закриваємо файл
                super().save(update_fields=['photo'])  # Оновлюємо тільки photo
            except Exception as e:
                # Логуйте помилку, але не переривайте збереження
                print(f"Error converting image: {e}")

    def __str__(self):
        return self.user.username
