from pathlib import Path
import os

from dotenv import load_dotenv


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

    # наши приложения
    "users",
    "tickets",
    "comments",
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
