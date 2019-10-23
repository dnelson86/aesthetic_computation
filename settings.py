"""
Django settings for Aesthetic Computation website.
To update static files:
  (1) sudo -s
  (2) python3 manage_ac.py collectstatic
  (3) exit
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False # change to False for production

ALLOWED_HOSTS = ['.aesthetic-computation.com']

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.admin',
    'pipeline',
    'aesthetic_computation',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATES = [
  {'BACKEND' : 'django.template.backends.django.DjangoTemplates',
   'DIRS' : [os.path.join(BASE_DIR,'templates')],
   'APP_DIRS' : True,
   'OPTIONS' : {
     'context_processors' : [
       'django.contrib.auth.context_processors.auth',
       'django.contrib.messages.context_processors.messages',
       'django.template.context_processors.static',
       'django.template.context_processors.request',
     ],
     'debug' : DEBUG
    }
  }
]

ROOT_URLCONF = 'aesthetic_computation.urls'

WSGI_APPLICATION = 'aesthetic_computation.wsgi.application'

MEDIA_ROOT = "/var/www/html/static/ac/projects/"
MEDIA_URL  = "https://www.aesthetic-computation.com/static/ac/projects/"

# Database config ( https://docs.djangoproject.com/en/1.6/ref/settings/#databases )
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangodb_ac',
        'USER': 'djangouser_ac',
        'PASSWORD': 'f98htnVR&(N=',
        'OPTIONS': {'unix_socket':'/var/lib/mysql/mysql.sock'}
    }
}

SECRET_KEY = '3krd+n2eu+%m+ax97u9djt_reffbd$*+uuk6x=+n71wx1ql)#^'

#ADMINS = (('Dylan Nelson','dnelson@mpa-garching.mpg.de'))
PREPEND_WWW = False # TODO: re-enable after real domain name

# Internationalization ( https://docs.djangoproject.com/en/1.6/topics/i18n/ )
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

PIPELINE = {
  'DISABLE_WRAPPER' : True,
  'STYLESHEETS' :  {
    'base' :  {
        'source_filenames' : ( 'ac/css/bootstrap.min.css',
                               'ac/css/style.css' ),
        'output_filename' : 'min/ac.css'
    },
  },
  'JAVASCRIPT' : {
    'base' : {
        'source_filenames' : ( 'ac/js/jquery.min.js',
                               'ac/js/site.js' ),
        'output_filename' : 'min/ac.js'
    },
  }
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

BASE_WEB_ADDR = "https://www.aesthetic-computation.com/"
STATIC_URL = "/static_dev/" # TODO: change to 'static/' for production
STATIC_ROOT = "/srv/www/html/static_dev/" # where collectstatic puts things (TODO: change to 'static/' for prod)
