from django import forms
from pagedown.widgets import PagedownWidget

from .models import Post


class PostForm(forms.ModelForm):


    class Meta:
        model = Post
        fields = [
            'title',
            'image',
            'content',
        ]

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=PagedownWidget(attrs={'class': 'form-control'}))

