from celery import shared_task
from mail_templated import EmailMessage
from django.conf import settings
from django.shortcuts import redirect
from accounts.models import CostumeUser
from datetime import datetime, timedelta


@shared_task
def send_email_forgetPassword(user_name, user_email, token):
    link = redirect("accounts:confirm-forget-password", token).url
    for host in settings.CORS_ALLOWED_ORIGINS:
        data = {"token": token, "name": user_name, "link": link, "host": host}
        email = EmailMessage(
            "incs/email/forget_password.tpl",
            data,
            settings.EMAIL_HOST_USER,
            [user_email],
        )
        email.send()


@shared_task
def send_email_activateUser(user_name, user_email, token):
    link = redirect("accounts:activate-user", token).url
    for host in settings.CORS_ALLOWED_ORIGINS:
        data = {"token": token, "name": user_name, "link": link, "host": host}
        email = EmailMessage(
            "incs/email/activate_user.tpl",
            data,
            settings.EMAIL_HOST_USER,
            [user_email],
        )
        email.send()


@shared_task
def delete_unverified_users():
    expire_time = datetime.now() - timedelta(minutes=30)
    CostumeUser.objects.filter(
        created__lt=expire_time, is_verify=False
    ).delete()
    print(
        "SHEDULED-TASK: unverified users (for more than 10 minute) are deleted"
    )
