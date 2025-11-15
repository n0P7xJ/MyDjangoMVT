from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image', None)
        if image and not image.name.lower().endswith('.webp'):
            raise forms.ValidationError('Only WEBP images are allowed!')
        return image
