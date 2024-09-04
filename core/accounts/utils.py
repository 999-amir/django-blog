# from mail_templated import EmailMessage
# from django.conf import settings
# from django.shortcuts import redirect

# def send_email_forgetPassword(to_user, token):
#     link = redirect('accounts:confirm-forget-password', token).url
#     for host in settings.CORS_ALLOWED_ORIGINS:
#         data = {
#             'token': token,
#             'name': to_user.name,
#             'link': link,
#             'host': host
#         }
#         email = EmailMessage('incs/email/forget_password.tpl', data, settings.EMAIL_HOST_USER, [to_user.email])
#         email.send()

# def send_email_activateUser(to_user, token):
#     link = redirect('accounts:activate-user', token).url
#     for host in settings.CORS_ALLOWED_ORIGINS:
#         data = {
#             'token': token,
#             'name': to_user.name,
#             'link': link,
#             'host': host
#         }
#         email = EmailMessage('incs/email/activate_user.tpl', data, settings.EMAIL_HOST_USER, [to_user.email])
#         email.send()
 '''
    this file has been disabled cause now it using celery to send-email ( checkout accounts/tasks.py )
 '''