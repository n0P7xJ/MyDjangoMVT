from django import forms
from .models import Dish

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'category', 'price', 'priority', 'image', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows':3, 'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'priority': forms.NumberInput(attrs={'class':'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'})
        }