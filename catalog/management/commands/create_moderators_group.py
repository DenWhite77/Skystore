from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу «Модератор продуктов» с нужными правами'

    def handle(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(Product)

        delete_permission = Permission.objects.get(
            codename='delete_product',
            content_type=content_type,
        )

        unpublish_permission = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type,
        )

        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        group.permissions.add(delete_permission, unpublish_permission)

        if created:
            self.stdout.write(self.style.SUCCESS('✅ Группа «Модератор продуктов» создана'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Группа уже существовала — права обновлены'))

        self.stdout.write(self.style.SUCCESS(
            f'Права: {delete_permission.codename}, {unpublish_permission.codename}'
        ))
