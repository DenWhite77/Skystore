from django.core.cache import cache

from .models import Category, Product


def get_products_by_category(category_slug):
    """
    Возвращает (category, products) для указанной категории по slug.
    Использует низкоуровневое кеширование с ключом category_{id}.
    TTL — 15 минут.
    """
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        return None, []

    cache_key = f'category_{category.id}'
    products = cache.get(cache_key)

    if products is None:
        products = list(
            Product.objects.filter(category=category, is_published=True)
            .select_related('category')
        )
        cache.set(cache_key, products, timeout=60 * 15)
        print(f'[CACHE] Список продуктов категории {category.id} загружен из БД')
    else:
        print(f'[CACHE] Список продуктов категории {category.id} из Redis')

    return category, products
