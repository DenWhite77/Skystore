import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

# Указываем кодировку явно
with open('catalog/fixtures/catalog.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'catalog', indent=2, stdout=f)

print('OK: catalog/fixtures/catalog.json записан в UTF-8')
