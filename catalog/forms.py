from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наименование'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),
        }
        labels = {
            'name': 'Наименование',
            'description': 'Описание',
            'image': 'Изображение',
            'category': 'Категория',
            'price': 'Цена',
        }
