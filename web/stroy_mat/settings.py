from configurations import Configuration, values
import os

import sys
import logging

from django.core.management.color import color_style


class DjangoColorsFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super(DjangoColorsFormatter, self).__init__(*args, **kwargs)
        self.style = self.configure_style(color_style())

    def configure_style(self, style):
        style.DEBUG = style.HTTP_NOT_MODIFIED
        style.INFO = style.HTTP_INFO
        style.WARNING = style.HTTP_NOT_FOUND
        style.ERROR = style.ERROR
        style.CRITICAL = style.HTTP_SERVER_ERROR
        return style

    def format(self, record):
        message = logging.Formatter.format(self, record)
        if sys.version_info[0] < 3:
            if isinstance(message, str):
                message = message.encode('utf-8')
        colorizer = getattr(self.style, record.levelname, self.style.HTTP_SUCCESS)
        return colorizer(message)


class Base(Configuration):
    # Django settings for test_project project.

    DEBUG = values.BooleanValue(True, environ=True)

    ADMINS = (
        ('panagoa', 'panagoa@ya.ru'),
    )

    MANAGERS = ADMINS

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '37xxs(x=2xntw=mmdde2_nj^+j=f0rw&y=*#i+&jh&9t5safe%'

    # SECURITY WARNING: don't run with debug turned on in production!
    # DEBUG = True

    ALLOWED_HOSTS = ['*']

    # Application definition

    INSTALLED_APPS = [
        'core',
        'order_app',
        'shipment_app',
        'smsnotify_app',
        'comment_app',
        'provider_app',
        'product_app',
        'customer_app',

        'discharge_app',
        'data_app',

        # 'grappelli',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'debug_toolbar',

        'django_tables2',
        'bootstrap3',
        'django_filters',
        'configurations',

        'haystack',
        'leaflet',
        'djgeojson',

        'notifications',

        'cacheops'
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'stroy_mat.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

    WSGI_APPLICATION = 'stroy_mat.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.10/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/1.10/topics/i18n/

    LANGUAGE_CODE = 'ru-RU'

    TIME_ZONE = 'Europe/Moscow'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.10/howto/static-files/

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')


class Dev(Base):
    DEBUG = True


class Prod(Base):
    DEBUG = True

    # EMAIL_BACKEND = 'django_ses.SESBackend'
    #
    # # These are optional -- if they're set as environment variables they won't
    # # need to be set here as well
    # AWS_SES_ACCESS_KEY_ID = 'AKIAJG66MUMB7Y46CE7A'
    # AWS_SES_SECRET_ACCESS_KEY = 'AuuBrTZiLranxcWlPxl3J+4x8iOiiwhuw0EG2KsCsoHq'
    #
    # # Additionally, if you are not using the default AWS region of us-east-1,
    # # you need to specify a region, like so:
    # AWS_SES_REGION_NAME = 'eu-west-1'
    # AWS_SES_REGION_ENDPOINT = 'email-smtp.eu-west-1.amazonaws.com'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'HOST': os.environ['DB_SERVICE'],
            'PORT': os.environ['DB_PORT']
        }
    }

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #         'NAME': os.environ['DB_NAME'],
    #         'USER': os.environ['DB_USER'],
    #         'PASSWORD': os.environ['DB_PASS'],
    #         'HOST': os.environ['DB_SERVICE'],
    #         'PORT': '5445'
    #     }
    # }

    # SECRET_KEY = os.environ['SECRET_KEY']

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': '{}:{}'.format(os.environ['ES_URL'], '9200'),
            'TIMEOUT': 10,
            'INDEX_NAME': 'haystack',
            'INCLUDE_SPELLING': True,
        },
    }

    HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

    LEAFLET_CONFIG = {
        # 'SPATIAL_EXTENT': (5.0, 44.0, 7.5, 46),
        'DEFAULT_CENTER': (55.76, 37.64),
        'DEFAULT_ZOOM': 8,
        'MIN_ZOOM': 3,
        'MAX_ZOOM': 18,
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }

    INTERNAL_IPS = ('127.0.0.1', '46.39.230.142', '46.39.230.119', '188.120.229.184', '172.17.0.6')

    # redis and cacheops
    CACHEOPS_REDIS = {
        'host': os.environ['REDIS_HOST'],  # redis-server is on same machine
        'port': 6379,  # default redis port
        'db': 1,  # SELECT non-default redis database
        # using separate redis db or redis instance
        # is highly recommended

        'password': 'redis',  # optional
    }

    CACHEOPS_DEFAULTS = {
        'timeout': 60 * 60
    }

    CACHEOPS = {
        'auth.user': {'ops': 'get', 'timeout': 60 * 15},
        '*.*': {},
        #'*.*': {'ops': 'all', 'timeout': 60 * 60 * 2},
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'colored': {
                '()': DjangoColorsFormatter,
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
                'datefmt': '%d/%b/%Y %H:%M:%S',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'colored',
            },

            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'debug.log'),
            },
        },
        'loggers': {
            # 'django.db.backends': {
            #     'level': 'DEBUG',
            #     'handlers': ['file'],
            # },

            'stroy_mat': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'INFO',
            },
        },

    }
