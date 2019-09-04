""" Main app(blogs) widgets """
from django import forms


class FileInputWithPreview(forms.ClearableFileInput):
    """" Preview Implementation"""
    template_name = 'blogs/widgets/file_input_with_preview.html'

    class Media:
        js = ['blogs/js/preview.js']

    def __init__(self, attrs=None, include_preview=False):
        super().__init__(attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += 'preview-marker'
        else:
            self.attrs['class'] = 'preview-marker'
        self.include_preview = include_preview

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'include_preview': self.include_preview,
        })
        return context
