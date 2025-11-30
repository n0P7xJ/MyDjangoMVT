from django.test import TestCase
from .models import Category

class CategoryModelTest(TestCase):
    def test_str_method(self):
        category = Category.objects.create(name="Салати")
        self.assertEqual(str(category), "Салати")

