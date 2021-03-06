"""
Django settings for tuling_malls project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os,sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8oq#c78aano6%jukvoqus*^r%t_-dc)+vu1*8u#rm_#acp5^n4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'corsheaders',
    'verification',
    'area',
    'goods',
    'haystack',
    'django_crontab',
    'cart',
    'pay',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tuling_malls.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'tuling_malls.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '192.168.88.2',  # ???????????????
        'PORT': 3306,  # ???????????????
        'USER': 'root',  # ??????????????????
        'PASSWORD': 'root',  # ?????????????????????
        'NAME': 'tuling_malls'  # ???????????????
    }
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "histories": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE='django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS='default'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ =  True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR,'statis')]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # ????????????????????????????????????
    'formatters': {  # ???????????????????????????
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # ?????????????????????
        # ???debug=True?????????
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # ??????????????????
        'console': {  # ????????????????????????
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # ????????????????????????
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/tuling_malls.logs'),  # ?????????????????????
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # ?????????
        'django': {  # ?????????????????????django????????????
            'handlers': ['console', 'file'],  # ?????????????????????????????????????????????
            'propagate': True,  # ??????????????????????????????
            'level': 'INFO',  # ????????????????????????????????????
        },
    }
}
CORS_ORIGIN_WHITELIST=(
    'http://127.0.0.1:8000',
    'http://localhost:8000',

    'http://127.0.0.1:8080',
    'http://localhost:8080',

    'http://192.168.88.2:8000',
    'http://192.168.88.2:8080',
)
CORS_ALLOW_CREDENTIALS=True
AUTH_USER_MODEL='user.User'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '13657284142@163.com' # ??????????????????
# ???????????????????????????????????????
EMAIL_HOST_PASSWORD = 'TVRXDQUTKSYVFEWU' # ?????????????????????
EMAIL_FROM = '????????????<13657284142@163.com>'

DEFAULT_FILE_STORAGE='utils.fastdfs.storage.MYstorage'

HAYSTACK_CONNECTIONS = {
    'default': {
    'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
    'URL': 'http://192.168.88.2:9200/', # Elasticsearch?????????ip???????????????????????????9200
    'INDEX_NAME': 'tuling_malls', # Elasticsearch???????????????????????????
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE=6

CRONJOBS = [
    ('*/1 * * * *', 'contents.crons.detail','>>'+os.path.join(BASE_DIR,'logs/crontab.log'))
]
ALIPAY_APPID = '2021000118686068'
ALIPAY_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'apps/pay/keys/app_private_key.pem')
ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'apps/pay/keys/app_public_key.pem')
ALIPAY_DEBUG = True
ALIPAY_SUBJECT = '????????????-????????????'
ALIPAY_RETURN_URL = 'http://127.0.0.1:8080/pay_success.html'
ALIPAY_GATE = 'https://openapi.alipaydev.com/gateway.do?'