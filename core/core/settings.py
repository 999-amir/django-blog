"""
settings.py
    - BASE
    - SECURITY
    - APPS
    - SERVER GRAPHIC INTERFACE
    - TEMPLATE
    - BACKGROUND PROCESS, BEAT, CACHE
    - DATABASE
    - FILE
    - etc
    - EMAIL
    - TIME
    - API
    - DEBUG
"""

# =================================================================| BASE
from datetime import timedelta
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# =================================================================| SECURITY
# SECURITY WARNING: keep the key used in production secret!
SECRET_KEY = config("SECRET_KEY")
CRYPTOGRAPHY_KEY = config("CRYPTOGRAPHY_KEY").encode(
    encoding="utf-8"
)

# SECURITY WARNING: keep the host after deployment!
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default="*",
)
SITE_ID = config("SITE_ID", cast=int, default=1)
if config("CORS_ALLOW_ALL_ORIGINS", cast=bool, default=False):
    CORS_ALLOW_ALL_ORIGINS=True
else:
    CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS").split(",")

# security configs for production
if config("USE_SSL_CONFIG", cast=bool, default=False):
    # Https settings
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # more security settings
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "SAMEORIGIN"
    SECURE_REFERRER_POLICY = "strict-origin"
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # optional
    "accounts.middleware.TrackingUserMiddleware",
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# CostumeUser
AUTH_USER_MODEL = "accounts.CostumeUser"


# =================================================================| APPS
INSTALLED_APPS = [
    # websocket
    "daphne",
    # base
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # installed_apps
    "accounts.apps.AccountsConfig",
    "home.apps.HomeConfig",
    "blog.apps.BlogConfig",
    "message.apps.MessageConfig",
    "private_data.apps.PrivateDataConfig",
    # api
    "rest_framework",
    "drf_yasg",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    # third party app
    "django_filters",
    "corsheaders",
    "mail_templated",
    # beat
    "django_celery_beat",
]


# =================================================================| SERVER GRAPHIC INTERFACE
ASGI_APPLICATION = "core.asgi.application"


# =================================================================| TEMPLATE
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # optional
                "home.context_processors.fast_access_links",
                "accounts.context_processors.track_users_seen",
            ],
        },
    },
]


# =================================================================| DATABASE
# Database
DATABASES = {
    "default": {
        "ENGINE": config("PGDB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("PGDB_NAME", default="postgres_name"),
        "USER": config("PGDB_USER", default="postgres_user"),
        "PASSWORD": config("PGDB_PASSWORD", default="postgres_password"),
        "HOST": config("PGDB_HOST", default="db"),
        "PORT": config("PGDB_PORT", cast=int, default=5432),
    }
}


# =================================================================| IN-MEMORY-DATABASE (redis)
# websocket-daphne
REDIS_CHANNELS_URL = config("REDIS_CHANNELS_URL")
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_CHANNELS_URL],
        },
    },
}

# worker-celery
CELERY_BROKER_URL = config('CELERY_BROKER_URL')

# cache
REDIS_CACHE_URL = config("REDIS_CACHE_URL")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CACHE_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}


# =================================================================| FILES
# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static/"
STATICFILES_DIRS = [BASE_DIR / "staticfiles"]

# media files (img)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

# whitenoise
if config("ENABLE_WHITENOISE", cast=bool, default=False):
    MIDDLEWARE += [
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]
    STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'

# =================================================================| etc
ROOT_URLCONF = "core.urls"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# coming-soon
COMINGSOON = config("COMINGSOON", cast=bool, default=False)


# =================================================================| DEBUG
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)
SHOW_DEBUGGER_TOOLBAR = config("SHOW_DEBUGGER_TOOLBAR", cast=bool, default=False)

# django debug toolbar for docker usage
if SHOW_DEBUGGER_TOOLBAR:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


# =================================================================| EMAIL
# Email Configurations for production and development
if DEBUG:    
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = False
    EMAIL_HOST = "smtp4dev"
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_PORT = 25
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = 587

EMAIL_REVERSE_DOMAIN=config("EMAIL_REVERSE_DOMAIN")

# =================================================================| TIME
# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = config("TIME_ZONE", default="UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True


# =================================================================| API
# restframework configurations
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}
if config("DISABLE_BROWSEABLE_API", cast=bool, default=False):
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (
        "rest_framework.renderers.JSONRenderer",)

# swagger configs
SHOW_SWAGGER = config("SHOW_SWAGGER", cast=bool, default=True)
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": True,
    "SECURITY_DEFINITIONS": [],
    "LOGIN_URL": "rest_framework:login",
    "LOGOUT_URL": "rest_framework:logout",
    "REFETCH_SCHEMA_ON_LOGOUT": True,
    "JSON_EDITOR": True,
}

# simple jwt settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
}
if config("FILE_DEBUGGER",cast=bool, default=True):
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(levelname)s %(asctime)s %(name)s.%(funcName)s:%(lineno)s- %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "log.django",
                "formatter": "simple",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": config("DJANGO_LOG_LEVEL", default="WARNING"),
                "propagate": True,
            },
        },
    }
