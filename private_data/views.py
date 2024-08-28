from django.shortcuts import render, redirect
from django.views import View
from .models import PrivateDataModel
from django.shortcuts import get_object_or_404
from django.contrib import messages


class PrivateDataView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'need registration', 'amber-600')
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
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, private_pk):
        private_data = get_object_or_404(PrivateDataModel, user=request.user, pk=private_pk)
        msg_text = f'USERNAME: {private_data.username}\n' \
                   f'PASSWORD: {private_data.password}'
        messages.error(request, msg_text, 'red-600')
        return redirect('private-data:main_page')
