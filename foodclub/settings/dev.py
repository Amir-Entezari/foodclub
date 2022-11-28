from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y77yt8rwn!8$fr!61s2l@ht5gr9!n=k@bd!1)4(+q+8&+42)sh'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'foodclub',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'A1050987136a@'
    }
}
