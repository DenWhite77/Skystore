from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ProductForm
from .models import Contact, Product


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    paginate_by = 3
    ordering = ('id',)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Модераторы видят всё, остальные — только опубликованное
        if self.request.user.is_authenticated and self.request.user.has_perm('catalog.can_unpublish_product'):
            return queryset
        return queryset.filter(is_published=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        can_edit = (
            request.user == product.owner
            or request.user.has_perm('catalog.change_product')
        )
        if not can_edit:
            raise PermissionDenied('Вы не можете редактировать чужой продукт.')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        can_delete = (
            request.user == product.owner
            or request.user.has_perm('catalog.delete_product')
        )
        if not can_delete:
            raise PermissionDenied('Вы не можете удалить чужой продукт.')
        return super().dispatch(request, *args, **kwargs)


class ProductUnpublishView(LoginRequiredMixin, View):
    """Модератор снимает/ставит публикацию продукта."""

    def post(self, request, pk):
        if not request.user.has_perm('catalog.can_unpublish_product'):
            raise PermissionDenied('У вас нет прав на снятие с публикации.')

        product = get_object_or_404(Product, pk=pk)
        product.is_published = not product.is_published
        product.save(update_fields=['is_published'])

        return redirect('catalog:product_detail', pk=pk)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact'] = Contact.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Обратная связь: {name} | {phone} | {message}')
        return self.render_to_response(self.get_context_data(success=True))
