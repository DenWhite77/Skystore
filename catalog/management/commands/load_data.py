from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Загрузка тестовых данных из фикстуры catalog.json'

    def handle(self, *args, **kwargs):
        # Предварительное удаление данных
        self.stdout.write('Удаление старых данных...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загрузка фикстуры
        self.stdout.write('Загрузка фикстуры catalog.json...')
        call_command('loaddata', 'catalog.json')

        # Отчёт
        self.stdout.write(
            self.style.SUCCESS(
                f'Готово! Загружено {Category.objects.count()} категорий '
                f'и {Product.objects.count()} продуктов.'
            )
        )
