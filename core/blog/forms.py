from django import forms
from .models import BlogModel


class CreateBlogTitleForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ('title', 'snippet', 'category')


class CreateBlogContentForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput, required=False)
    file = forms.FileField(required=False)
