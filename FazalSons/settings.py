from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PRODUCT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a!*(fow%l)n7(6_g#jj8+8%=$v&^h+&-(wb%zu2^92b30l1&#q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000'
] ### For CORS Headers

# INTERNAL_IPS = [ 
#     '127.0.0.1',  
# ] ### For Django Debug Toolbar

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders', ### For CORS Headers
    # 'debug_toolbar', ### For Django Debug Toolbar
    'AppProduct',
    'AppCustomer',
    'AppStock',
    'AppAccount',
    'AppPOS',
    'AppReport',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # Here
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware', ### For CORS Headers
    # 'debug_toolbar.middleware.DebugToolbarMiddleware', ### For Django Debug Toolbar
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FazalSons.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PRODUCT_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'FazalSons.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'db_fazal_sons_pos',
    #     'USER': 'postgres',
    #     'PASSWORD': '123',
    #     'PORT': '5432',
    #     'HOST': 'localhost',
    # }

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_fazal_sons_pos',
        'USER': 'postgres',
        'PASSWORD': 'Naveed*123',
        'PORT': '5432',
        'HOST': 'fazalsons.ctsg24aca9u5.eu-north-1.rds.amazonaws.com',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Karachi'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# STATIC_ROOT = '/home/ubuntu/project/Fazal-Sons-POS/static/'
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(PRODUCT_DIR, "static"), '/home/ubuntu/project/Fazal-Sons-POS/static/',
]

# STATIC_URL = '/static/'
# STATIC_ROOT = ''
# STATICFILES_DIRS = (
#     '/home/ubuntu/project/Fazal-Sons-POS/static',
# )

# STATICFILES_DIRS = [
#     os.path.join(PRODUCT_DIR, 'static')
# ]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_ROOT = os.path.join(PRODUCT_DIR, 'media')
MEDIA_URL = '/media/'

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         # 'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#     ]
# }


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}
