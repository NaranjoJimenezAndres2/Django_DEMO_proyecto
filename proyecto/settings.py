"""
Django settings for proyecto project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(f!gc7&yt$sq3h8$g%ihj$jx2kje)++$ft-hbt&@(*c5tvdoxq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'proyecto',
    
    
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    
    # Django REST framework 
    'rest_framework',
    
    # ForumlaOne application
    'formulaOne.apps.FormulaOneConfig',
    
    # Prueba application
    'prueba.apps.PruebaConfig',
    
    # Comparacion application
    'comparacionDjango.apps.ComparaciondjangoConfig',

    
    
    # CORS
    'corsheaders',
    
    #Heroku
    'whitenoise.runserver_nostatic',
    
    #Boostrap
    'bootstrap4',
    
    #'fastf1'
    

    

    
]

MIDDLEWARE = [
    
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    #--------
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
       # Add whitenoise middleware here
   'whitenoise.middleware.WhiteNoiseMiddleware',
    
 
    
    
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
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}
MONGO_URI ='mongodb+srv://empresa:0000@cluster0.oxux9.mongodb.net/proyecto?retryWrites=true&w=majority'
 
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'proyecto',
        'ENFORCE_SCHEMA': False,
        "CLIENT": {
           "host": 'mongodb+srv://empresa:0000@cluster0.oxux9.mongodb.net/proyecto?retryWrites=true&w=majority',
        }, 
    }
}
 

CORS_ORIGIN_ALLOW_ALL = True

#CORS_ORIGIN_WHITELIST = (
#       'http://localhost:4500',
#)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#ALLOWED_HOSTS = ['localhost', '.herokuapp.com']
ALLOWED_HOSTS = ['localhost', '.herokuapp.com']

DEBUG = True

CRISPY_TEMPLATE_PACK = 'uni_form'



CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'C:/Users/diama/Desktop/proyecto final FP_2/hello_django',
    }
}




