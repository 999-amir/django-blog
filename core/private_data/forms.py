from django import forms


class CreateNewPrivateDataForm(forms.Form):
    title = forms.CharField(max_length=250)
    username = forms.CharField(max_length=250)
    password = forms.CharField(widget=forms.PasswordInput)
