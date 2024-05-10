"""
Django settings for shoppinglyx project.

Generated by 'django-admin startproject' using Django 4.1.12.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-@7i(hej*mx!5tpwoyjjc9ghmu=is_t#zieb-9xkq+7ch)$i2%o"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

EXTERNAL_APPS = [
    "app",
    "social_django",
]

INSTALLED_APPS += EXTERNAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",  # <-- Here
]

ROOT_URLCONF = "shoppinglyx.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",  # <-- Here
                "social_django.context_processors.login_redirect",  # <-- Here
            ],
        },
    },
]

WSGI_APPLICATION = "shoppinglyx.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": "shoppinglyx",
        "ENFORCE_SCHEMA": True,
        "HOST": "localhost",
        "PORT": 27017,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Some External Added Code

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
LOGIN_REDIRECT_URL = "/"

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"  # get reset password in in console
)


# Email Configuration

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'  # SMTP server
# EMAIL_PORT = 587  # Port for sending email
# EMAIL_USE_TLS = True  # Whether to use TLS (secure connection)
# EMAIL_HOST_USER = 'yashum0089@gmail.com'  # Sender's email
# EMAIL_HOST_PASSWORD = 'Jorda'


# Payment

RAZORPAY_KEY_ID = "rzp_test_bdEZ8a1mK96ALp"
RAZORPAY_KEY_SECRET = "RHGV8JDa6OPjYX4lrFbbmy38"


# Social Auth

AUTHENTICATION_BACKENDS = (
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.twitter.TwitterOAuth",
    "social_core.backends.github.GithubOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_FACEBOOK_KEY = "935692644596098"
SOCIAL_AUTH_FACEBOOK_SECRET = "a9e05d34144e336075e6709d40bcb22c"

SOCIAL_AUTH_TWITTER_KEY = "qdHfceLe35GyZ6mUUqdjrqQbN"
SOCIAL_AUTH_TWITTER_SECRET = "1jsSZQvwSfGCbVCEQQ2LROVj04sE11s2cmmXOEor5JIkGQcfLy"


SOCIAL_AUTH_GITHUB_KEY = "88962c65907375a83557"
SOCIAL_AUTH_GITHUB_SECRET = "b4bd13b4df3a05f2cf5c6b0b4b9ba72a556815f0"