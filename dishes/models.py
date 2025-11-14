import os
import uuid
from django.db import models
from django.utils.deconstruct import deconstructible

@deconstructible
class UniqueWebpPath(object):
    def __call__(self, instance, filename):
        ext = 'webp'
        unique_name = f'{uuid.uuid4().hex}.{ext}'
        return os.path.join('category_images/', unique_name)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=UniqueWebpPath(), blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']
        