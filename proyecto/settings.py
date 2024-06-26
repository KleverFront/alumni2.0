"""
Django settings for proyecto project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config
from django.urls import reverse_lazy
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-zf9893yw6_lpv^6m5^b9+-bx2p$1#iktijv*burgruui9@@2fk'
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG_STATUS")

ALLOWED_HOSTS = ['alumni.tecnologicoloja.edu.ec','10.200.2.138','localhost']


# Application definition

INSTALLED_APPS = [
    'aplicacion',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'widget_tweaks',
    'django.contrib.humanize',
    'compressor',
    'rest_framework.authtoken',
    'tinymce',
       
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

ROOT_URLCONF = 'proyecto.urls'

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

WSGI_APPLICATION = 'proyecto.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME, ## nombre de la base de datos
        'USER': DB_USER, 
        'PASSWORD': DB_PASSWORD, ## Se debe ajustar aqui la base de datos 
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'aplicacion.UsuarioBase'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

]

TINYMCE_DEFAULT_CONFIG = {
    'theme': 'silver',
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'plugins': '''
                textcolor save link image media preview codesample contextmenu
                table code lists fullscreen insertdatetime media pagebreak
                nonbreaking anchor toc bullist numlist outdent indent
                filemanager
                ''',
    'toolbar1': '''
                bold italic underline strikethrough |
                alignleft aligncenter alignright alignjustify |
                bullist numlist outdent indent |
                link image media |
                codesample |
                fullscreen preview
                ''',
    'toolbar2': '''
                forecolor backcolor |
                removeformat |
                subscript superscript |
                fontselect fontsizeselect |
                table |
                ''',
    'menubar': True,
    'statusbar': True,
}


TINYMCE_COMPRESSOR = True
TINYMCE_FILE_picker_callback = 'filemanager'


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es-ec'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/ingresar/'
LOGIN_REDIRECT_URL=reverse_lazy('index')
LOGOUT_REDIRECT_URL = '/alumni'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# IMPORT_EXPORT_USE_TRANSACTIONS = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'media'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = [
    'proyecto.custom_backend.MiAuthBackend',
    'django.contrib.auth.backends.ModelBackend', 
]

EMAIL_USER = config("EMAIL_USER")
EMAIL_PASS = config("EMAIL_PASS")
# CONFIGURACION DE EMAIL
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = EMAIL_USER ##correo que hara de la aplicacion de alumni
EMAIL_HOST_PASSWORD = EMAIL_PASS ##contraseña se recomienda revisar documentacion para esto

