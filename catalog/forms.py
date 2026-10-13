from django import forms
from django.core.exceptions import ValidationError

from .models import Product


FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')
        labels = {
            'name': 'Наименование',
            'description': 'Описание',
            'image': 'Изображение',
            'category': 'Категория',
            'price': 'Цена',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация всех полей формы
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        """Проверка имени на запрещённые слова."""
        name = self.cleaned_data.get('name', '')
        return self._check_forbidden_words(name, 'Наименование')

    def clean_description(self):
        """Проверка описания на запрещённые слова."""
        description = self.cleaned_data.get('description', '')
        return self._check_forbidden_words(description, 'Описание')

    def _check_forbidden_words(self, text, field_label):
        """Общая логика проверки запрещённых слов (регистр игнорируется)."""
        text_lower = text.lower()
        for word in FORBIDDEN_WORDS:
            if word in text_lower:
                raise ValidationError(
                    f'В поле «{field_label}» запрещено использовать слово «{word}».'
                )
        return text

    def clean_price(self):
        """Проверка, что цена не отрицательная."""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        return price

    def clean_image(self):
        """Проверка формата и размера изображения (доп. задание)."""
        image = self.cleaned_data.get('image')
        if not image:
            return image

        # Если картинка уже была у товара и её не меняли — пропускаем проверку
        if not hasattr(image, 'content_type'):
            return image

        # Проверка формата
        allowed_types = ('image/jpeg', 'image/png')
        if image.content_type not in allowed_types:
            raise ValidationError('Допустимы только файлы формата JPEG или PNG.')

        # Проверка размера (не более 5 МБ)
        max_size = 5 * 1024 * 1024
        if image.size > max_size:
            raise ValidationError('Размер файла не должен превышать 5 МБ.')

        return image
