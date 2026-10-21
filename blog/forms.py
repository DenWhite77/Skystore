from django import forms

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'preview', 'is_published')
        labels = {
            'title': 'Заголовок',
            'content': 'Содержимое',
            'preview': 'Превью',
            'is_published': 'Опубликовано',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
