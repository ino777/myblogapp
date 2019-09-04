""" Main app(blogs) form """
from django import forms


from .models import Post
from .widgets import FileInputWithPreview


class PostForm(forms.ModelForm):
    """ Post form """

    class Meta:
        model = Post
        fields = ('title', 'text', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'rows':1, 'cols': 50, 'id': 'title_form'}),
            'text': forms.Textarea(attrs={'rows': 10, 'cols': 80, 'max-rows': 50, 'id': 'text_form'}),
            'image': FileInputWithPreview,
        }
