from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Contact, Product


def home(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 3)  # по 3 продукта на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for product in page_obj:
        print(f'{product.id} | {product.name} | {product.category.name} | {product.price}')

    return render(request, 'catalog/home.html', {'page_obj': page_obj})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})


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
