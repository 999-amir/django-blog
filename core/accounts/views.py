from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from .models import CostumeUser, TrackingUserModel
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from .incs import check_signup_data, check_password_strength
from .tasks import send_email_forgetPassword, send_email_activateUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import jwt
from django.shortcuts import get_object_or_404


class SignupView(View):
    form_class = SignupForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'you are already authenticated', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        forms = self.form_class()
        messages.success(request, 'example for password: Aaa123$$', 'cyan-600')
        return render(request, 'accounts/SIGNUP.html', {'forms': forms})

    def post(self, request):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            check_response = check_signup_data(cd['name'], cd['email'], cd['password_1'], cd['password_2'])
            if not check_response['mode']:
                messages.warning(request, check_response['message'], 'cyan-600')
                return render(request, 'accounts/SIGNUP.html', {'forms': forms})
            user = CostumeUser.objects.create_user(name=cd['name'], email=cd['email'], password=cd['password_1'])
            login(request, user)
            messages.success(request, 'user created, you have 30 minutes to verify your account', 'cyan-600')
            return redirect('home:main_page')
        messages.success(request, 'example for password: Aaa123$$', 'green-600')
        return render(request, 'accounts/SIGNUP.html', {'forms': forms})


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'need registration', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        messages.success(request, 'logout completed', 'green-600')
        return redirect('home:main_page')


class LoginView(View):
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'you are already authenticated', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        forms = self.form_class
        return render(request, 'accounts/LOGIN.html', {'forms': forms})

    def post(self, request):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'login completed', 'green-600')
                return redirect('home:main_page')
            messages.warning(request, 'username or password is wrong', 'cyan-600')
            return render(request, 'accounts/LOGIN.html', {'forms': forms})
        return render(request, 'accounts/LOGIN.html', {'forms': forms})


class ChangePasswordView(View):
    form_class = ChangePasswordForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'need registration', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        forms = self.form_class()
        messages.success(request, 'example for password: Aaa123$$', 'cyan-600')
        return render(request, 'accounts/CHANGE-PASSWORD.html', {'forms': forms})

    def post(self, request):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            check_old_password = request.user.check_password(cd['old_password'])
            if check_old_password:
                check_response = check_password_strength(cd['new_password1'], cd['new_password2'])
                if check_response['mode']:
                    request.user.set_password(cd['new_password1'])
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'password-changed and logged in', 'green-600')
                    return redirect('home:main_page')
                else:
                    messages.warning(request, check_response['message'], 'cyan-600')
                    return render(request, 'accounts/CHANGE-PASSWORD.html', {'forms': forms})
            messages.warning(request, 'previous password is incorrect [ you can use change-password ]', 'cyan-600')
            return render(request, 'accounts/CHANGE-PASSWORD.html', {'forms': forms})
        return render(request, 'accounts/CHANGE-PASSWORD.html', {'forms': forms})


class SendForgetPasswordTokenView(View):
    form_class = SendForgetPasswordTokenForm

    def get(self, request):
        forms = self.form_class()
        return render(request, 'accounts/forget-password/SEND-FORGET-PASSWORD.html', {'forms': forms})

    def post(self, request):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data['email']
            user = CostumeUser.objects.filter(email=email)
            if not user.exists():
                messages.warning(request, 'user does not exist', 'orange-600')
                return render(request, 'accounts/forget-password/SEND-FORGET-PASSWORD.html', {'forms': forms})
            user = user.first()
            token = self.get_token_for_user(user)
            send_email_forgetPassword.delay(user.name, user.email, token)
            messages.success(request, 'check your email', 'green-600')
            return redirect('home:main_page')
        return render(request, 'accounts/forget-password/SEND-FORGET-PASSWORD.html', {'forms': forms})

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ConfirmForgetPasswordView(View):
    form_class = ConfirmForgetPasswordForm

    def get(self, request, token):
        forms = self.form_class()
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            messages.warning(request, 'token has been expired', 'green-600')
            return render(request, 'accounts/forget-password/CONFIRM-FORGET-PASSWORD.html', {'forms': forms})
        except jwt.InvalidSignatureError:
            messages.warning(request, 'token is invalid', 'green-600')
            return render(request, 'accounts/forget-password/CONFIRM-FORGET-PASSWORD.html', {'forms': forms})
        except:
            messages.warning(request, 'incorrect token', 'green-600')
            return render(request, 'accounts/forget-password/CONFIRM-FORGET-PASSWORD.html', {'forms': forms})
        return render(request, 'accounts/forget-password/CONFIRM-FORGET-PASSWORD.html', {'forms': forms})

    def post(self, request, token):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            try:
                token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = token.get('user_id')
            except jwt.ExpiredSignatureError:
                messages.warning(request, 'token has been expired', 'green-600')
                return render(request, 'accounts/forget-password/CONFIRM-FORGET-PASSWORD.html', {'forms': forms})
            except jwt.InvalidSignatureError:
                messages.warning(request, 'token is invalid', 'green-600')
                return render(request, 'accounts/forget-password/CONFIRM-FORGET-PASSWORD.html', {'forms': forms})
            except:
                messages.warning(request, 'incorrect token', 'green-600')
                return render(request, 'accounts/forget-password/CONFIRM-FORGET-PASSWORD.html', {'forms': forms})
            check_response = check_password_strength(cd['new_password1'], cd['new_password2'])
            if not check_response['mode']:
                messages.warning(request, check_response['message'], 'cyan-600')
            user = get_object_or_404(CostumeUser, pk=user_id)
            if not user.is_verify:
                user.is_verify = True
                user.save()
            user.set_password(cd['new_password1'])
            for track in TrackingUserModel.objects.filter(user=user):
                track.user = None
                track.save()
            user.save()
            messages.success(request, 'password changed successfully', 'cyan-600')
            return redirect('home:main_page')
        return render(request, 'accounts/forget-password/CONFIRM-FORGET-PASSWORD.html', {'forms': forms})


class SendActivateTokenView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'please login for send you activation-email with authenticated user', 'amber-600')
            return redirect('home:main_page')
        elif request.user.is_verify:
            messages.error(request, 'your account has been verified before', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        token = self.get_token_for_user(request.user)
        send_email_activateUser.delay(request.user.name, request.user.email, token)
        messages.success(request, 'email send', 'green-600')
        return redirect('home:main_page')

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivateUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'please login for send you activation-email with authenticated user', 'amber-600')
            return redirect('home:main_page')
        elif request.user.is_verify:
            messages.error(request, 'your account has been verified before', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, token):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except jwt.ExpiredSignatureError:
            messages.error(request, 'token has been expired', 'amber-600')
            return redirect('home:main_page')
        except jwt.InvalidSignatureError:
            messages.error(request, 'token is invalid', 'amber-600')
            return redirect('home:main_page')
        except:
            messages.error(request, 'token is incorrect', 'amber-600')
            return redirect('home:main_page')
        user = get_object_or_404(CostumeUser, pk=user_id)
        if user.id != request.user.id:
            messages.error(request, 'the user that receive email is not the same with user who authenticated', 'amber-600')
            return redirect('home:main_page')
        user.is_verify = True
        user.save()
        messages.success(request, 'user activated', 'green-600')
        return redirect('home:main_page')
