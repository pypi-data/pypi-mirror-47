import os
from django.utils.translation import ugettext_lazy as _

DEBUG = True
SECRET_KEY = "tests"
ROOT_URLCONF = "tests.urls"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
INSTALLED_APPS = (
    "django.contrib.sessions",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "sampleapp",
    "modelformhistory",
    "django_nose",
)
# TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [os.path.dirname(__file__)],
        "OPTIONS": {
            "context_processors": (
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            )
        },
    }
]
MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
)
LOGIN_REDIRECT_URL = "/"

USE_I18N = True
LANGUAGE_CODE = "en"

LANGUAGES = (("en", _("English")), ("fr", _("French")))
