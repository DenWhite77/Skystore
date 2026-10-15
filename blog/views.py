from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import BlogPostForm
from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blogposts'
    queryset = BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blogpost'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])

        if obj.views_count == 100:
            send_mail(
                subject=f'Поздравляем! Статья «{obj.title}» набрала 100 просмотров',
                message=(
                    f'Ваша статья «{obj.title}» достигла 100 просмотров!\n\n'
                    f'Ссылка: /blogs/{obj.pk}/\n\n'
                    f'Skystore'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['admin@skystore.local'],
                fail_silently=True,
            )

        return obj


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm          # ← было fields = (...)
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:blogpost_list')


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm          # ← было fields = (...)
    template_name = 'blog/blogpost_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:blogpost_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:blogpost_list')
