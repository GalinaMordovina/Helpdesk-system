from pathlib import Path
import os

from dotenv import load_dotenv
from datetime import timedelta


# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent
# Загружаем переменные окружения из файла .env
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")

# Режим отладки:
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Список разрешённых хостов
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # сторонние
    "rest_framework",
    "drf_spectacular",
    "django_filters",

    # наши приложения
    "users",
    "tickets",
    "comments",
    "statistics_app",
    "notifications",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# База данных
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # Движок базы данных
        "NAME": os.getenv("POSTGRES_DB"),  # Имя базы данных
        "USER": os.getenv("POSTGRES_USER"),  # Пользователь
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),  # Пароль пользователя
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Локализация
LANGUAGE_CODE = 'ru'         # язык интерфейса

TIME_ZONE = 'Europe/Moscow'  # часовой пояс

USE_I18N = True

USE_TZ = True


# Статические и медиа-файлы
STATIC_URL = 'static/'

# Это настройка Django, которая определяет тип поля первичного ключа (id)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Кастомная модель пользователя
AUTH_USER_MODEL = "users.User"

# Настройки Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",          # отдаёт ответы в JSON
        "rest_framework.renderers.BrowsableAPIRenderer",  # включает красивую HTML-страницу DRF
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (                   # токены Bearer
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

    "DEFAULT_FILTER_BACKENDS": [                          # фильтр, поиск
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],

}


# Настройки drf-spectacular
SPECTACULAR_SETTINGS = {
    # Название API
    "TITLE": "HelpDesk System API",

    # Описание API
    "DESCRIPTION": (
        "Автодокументация API информационной системы управления "
        "заявками технической поддержки. "
        "Основные разделы: users, tickets, comments, auth."
    ),

    # Версия API
    "VERSION": "1.0.0",

    # Не показывать отдельный endpoint схемы в Swagger
    "SERVE_INCLUDE_SCHEMA": False,

    # Кнопка Authorize для JWT
    "SECURITY_SCHEMES": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    },

    "SECURITY": [{"BearerAuth": []}],

    # Настройки Swagger UI
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "filter": True,
    },
}

# Email notifications
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)


# Увеличим lifetime для проверки
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
