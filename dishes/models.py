from django.db import models
from categories.models import Category
from common.models import UniqueWebpPath

class Dish(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    priority = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to=UniqueWebpPath(), blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dish"
        verbose_name_plural = "Dishes"
        ordering = ['priority', 'name']
