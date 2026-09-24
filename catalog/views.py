from django.shortcuts import render

from .models import Contact, Product


def home(request):
    products = Product.objects.order_by('-created_at')[:5]
    for product in products:
        print(f'{product.id} | {product.name} | {product.category.name} | {product.price}')
    return render(request, 'catalog/home.html', {'products': products})


def contacts(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Обратная связь: {name} | {phone} | {message}')
        success = True
    contact = Contact.objects.first()
    return render(request, 'catalog/contacts.html', {
        'success': success,
        'contact': contact,
    })
