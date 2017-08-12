from configurations import Configuration, values
import os


class Base(Configuration):
    # Django settings for test_project project.

    DEBUG = values.BooleanValue(True, environ=True)

    ADMINS = (
        ('panagoa', 'panagoa@ya.ru'),
    )

    EMAIL_URL = values.EmailURLValue('console://', environ=True)

    MANAGERS = ADMINS

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '37xxs(x=2xntw=mmdde2_nj^+j=f0rw&y=*#i+&jh&9t5safe%'

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
        'has_app.apps.HasAppConfig',

        'django_tables2',
        'bootstrap3',
        'django_filters',
        'configurations',

        'haystack',
        'leaflet',
        'djgeojson',
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
            'URL': '{}:{}'.format('194.67.215.206', '9200'),
            'TIMEOUT': 60 * 5,
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
