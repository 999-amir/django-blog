from django import forms


class CreateBlogTitleForm(forms.Form):
    title = forms.CharField(max_length=20)
    snippet = forms.CharField(max_length=250)


class CreateBlogContentForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput, required=False)
    file = forms.FileField(required=False)
