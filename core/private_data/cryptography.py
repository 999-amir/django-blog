from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.CRYPTOGRAPHY_KEY)


def encrypt(text):  # str[text] -> byte[text] -> encode -> str[token]
    byten_text = text.encode(encoding="utf-8")
    byten_encrypt = fernet.encrypt(byten_text)
    str_token = byten_encrypt.decode(encoding="utf-8")
    return str_token


def decrypt(token):  # str[token] -> byte[token] -> decode -> str[text]
    byten_token = token.encode(encoding="utf-8")
    byten_decrypt = fernet.decrypt(byten_token)
    str_text = byten_decrypt.decode(encoding="utf-8")
    return str_text
