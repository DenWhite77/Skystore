from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .forms import ProductForm
from .models import Category


class HomePageTest(TestCase):
    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_contacts_page_status(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)


class ProductFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Тестовая категория')

    def _form_data(self, **overrides):
        """Базовые данные формы + переопределения."""
        data = {
            'name': 'Обычный товар',
            'description': 'Обычное описание',
            'category': self.category.pk,
            'price': 100,
        }
        data.update(overrides)
        return data

    # === Запрещённые слова в name ===

    def test_forbidden_word_in_name(self):
        form = ProductForm(data=self._form_data(name='Казино удачи'))
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_forbidden_word_in_name_uppercase(self):
        form = ProductForm(data=self._form_data(name='КАЗИНО'))
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_forbidden_word_in_name_mixed_case(self):
        form = ProductForm(data=self._form_data(name='КаЗиНо'))
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    # === Запрещённые слова в description ===

    def test_forbidden_word_in_description(self):
        form = ProductForm(data=self._form_data(description='Это биржа какая-то'))
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_forbidden_word_in_description_uppercase(self):
        form = ProductForm(data=self._form_data(description='ОБМАН'))
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    # === Валидные данные ===

    def test_form_valid_without_forbidden_words(self):
        form = ProductForm(data=self._form_data())
        self.assertTrue(form.is_valid())

    # === Валидация цены ===

    def test_negative_price(self):
        form = ProductForm(data=self._form_data(price=-100))
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_zero_price_is_valid(self):
        form = ProductForm(data=self._form_data(price=0))
        self.assertTrue(form.is_valid())

    # === Валидация изображения ===

    def test_image_wrong_format(self):
        """PDF-файл должен быть отклонён."""
        pdf = SimpleUploadedFile(
            'test.pdf',
            b'%PDF-1.4 fake pdf content',
            content_type='application/pdf',
        )
        form = ProductForm(
            data=self._form_data(),
            files={'image': pdf},
        )
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)

    def test_image_too_large(self):
        """Файл больше 5 МБ должен быть отклонён."""
        # Создаём fake JPEG размером > 5 МБ
        big_content = b'\xff\xd8\xff\xe0' + b'0' * (6 * 1024 * 1024)
        big_image = SimpleUploadedFile(
            'big.jpg',
            big_content,
            content_type='image/jpeg',
        )
        form = ProductForm(
            data=self._form_data(),
            files={'image': big_image},
        )
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)
