from django.shortcuts import render, redirect
from django.views import View
from .models import PrivateDataModel
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .cryptography import encrypt, decrypt
from .forms import CreateNewPrivateDataForm

class PrivateDataView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'need registration', 'amber-600')
            return redirect('home:main_page')
        elif not request.user.is_verify:
            messages.error(request, 'please activate your account', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        private_data = PrivateDataModel.objects.filter(user=request.user)
        context = {
            'private_data': private_data
        }
        return render(request, 'private_data/PRIVATE_DATA.html', context)


class PrivateDataDetailView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'need registration', 'amber-600')
            return redirect('home:main_page')
        elif not request.user.is_verify:
            messages.error(request, 'please activate your account', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, private_pk):
        private_data = get_object_or_404(PrivateDataModel, user=request.user, pk=private_pk)
        msg_text = f'USERNAME: {decrypt(private_data.username)}<br>PASSWORD: {decrypt(private_data.password)}'
        messages.success(request, msg_text, 'red-600')
        return redirect('private-data:main_page')


class CreateNewPrivateDataView(View):
    form_class = CreateNewPrivateDataForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'need registration', 'amber-600')
            return redirect('home:main_page')
        elif not request.user.is_verify:
            messages.error(request, 'please activate your account', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        forms = self.form_class()
        return render(request, 'private_data/CREATE_NEW.html', {'forms': forms})

    def post(self, request):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            PrivateDataModel.objects.create(user=request.user, title=cd['title'], username=encrypt(cd['username']), password=encrypt(cd['password']))
            messages.success(request, 'username and password saved', 'green-600')
            return redirect('private-data:main_page')
        return render(request, 'private_data/CREATE_NEW.html', {'forms': forms})
