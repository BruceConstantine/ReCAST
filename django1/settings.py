"""
Django settings for django1 project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vb63*j5hv7(d0a&&be!_r4$(da4#$_qwbs3$mp^f+3&g9(so&='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # False True  # False # False

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # PyCharm Automaticly install ReCAST application -> ReCAST is a component in Django.
    'ReCAST.apps.RecastConfig',
]

# MIDDLEWARE_CLASSES in Django2.X
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ReCAST.middleware.URLMiddleware'
]

ROOT_URLCONF = 'django1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        # 设置为False， 不再去每个app下找templates文件，会在DIRS指定的路径寻找
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'ReCAST.config.static_file_dir',
                'ReCAST.config.navbar_paths',
                'ReCAST.config.options_paths',
                'ReCAST.config.helpNotDisplay_paths'
            ],
        },
    },
]

WSGI_APPLICATION = 'django1.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = 'static' # 新增行
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"static/")
   #, '/var/www/static/'
]
#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')  # 新增行
#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')  # 新增行


#print(STATICFILES_DIRS)
print(BASE_DIR)
print(os.path.join(BASE_DIR, '/static/'))
#print(STATIC_ROOT)

SESSION_CACHE_ALIAS = 'default'  # Cache to store session data if using the cache session backend.
SESSION_COOKIE_NAME = 'sessionid'  # Cookie name. This can be whatever you want.
SESSION_COOKIE_AGE = 60 * 5  # Age of cookie, in seconds (default: 2 weeks). Now is 5 minutes.
SESSION_COOKIE_DOMAIN = None  # A string like ".example.com", or None for standard domain cookie.
SESSION_COOKIE_SECURE = False  # Whether the session cookie should be secure (https:// only).
SESSION_COOKIE_PATH = '/'  # The path of the session cookie.
SESSION_COOKIE_HTTPONLY = True  # Whether to use the non-RFC standard httpOnly flag (IE, FF3+, others)
SESSION_SAVE_EVERY_REQUEST = False  # Whether to save the session data on every request.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Whether a user's session cookie expires when the Web browser is closed.
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # The module to store session data
SESSION_FILE_PATH = None  # Directory to store session files if using the file session module. If None, the backend will use a sensible default.
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'  # class to serialize session data

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
# EMAIL_USE_SSL = False
EMAIL_HOST = 'smtp.126.com'  # 如果是 qq 改成 smtp.qq.com
EMAIL_PORT = 25
EMAIL_HOST_USER = 'ZhikangTian@126.com'  # 帐号
EMAIL_HOST_PASSWORD = 'PGZZAHUXKFMBJNLA'  # 密码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
