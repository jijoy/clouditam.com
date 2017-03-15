"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.1.10

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.contrib.messages import constants

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')lsmbbo7ivr%8$bvgf1*77g9+lv4p^=^2l1qsb0%u=*co*!38$'

# SECURITY WARNING: don't run with debug turned on in production!
DEVELOPMENT = False

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cities_light',
    'ckeditor',
    'django_activeurl',
    'social.apps.django_app.default',
    'dashboard',
    'web',
    'api',
    'ecommerce',
    'rest_framework',
    'auditlog',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'app.middleware.ProtectAdminMiddleware',
)

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
                'dashboard.context_processors.bar'
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DEBUG = False
if DEVELOPMENT:
    DEBUG = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
elif not DEVELOPMENT:
    DEBUG = False
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '34o3RsDxT6D1_DB',
            'USER': 'ubuntu',
            'PASSWORD': '12qwaszxcv!',
            'HOST': '10.1.29.19',
            'PORT': '5432',
        }
    }

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ["*"]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'web/media')

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.linkedin.LinkedinOAuth',
    'django.contrib.auth.backends.ModelBackend',

)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    # Verifies that the social association can be disconnected from the current
    # user (ensure that the user login mechanism is not compromised by this
    # disconnection).
    'social.pipeline.disconnect.allowed_to_disconnect',

    # Collects the social associations to disconnect.
    'social.pipeline.disconnect.get_entries',

    # Revoke any access_token when possible.
    'social.pipeline.disconnect.revoke_tokens',

    # Removes the social associations.
    'social.pipeline.disconnect.disconnect',
)

######### SOCIAL AUTH #################
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '175127306832-c3q5iqsflng4jkk75igjjtohi45ugm1g.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '5Zd0jqqhPMjvRv8A3GZ_LKNj'
SOCIAL_AUTH_TWITTER_KEY = '7XXd7YMKIFSykqPBpZIthL83N'
SOCIAL_AUTH_TWITTER_SECRET = 'ooFgZ30dogEdHW0PDgzvoPHIebTNd50uv02OOtKobB0bKccIbk'
SOCIAL_AUTH_LINKEDIN_KEY = '77nqv1tns8rdkr'
SOCIAL_AUTH_LINKEDIN_SECRET = '531gpI7qJaEsCaZA'
SOCIAL_AUTH_LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress']
# Add the fields so they will be requested from linkedin.
SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = ['email-address', ]
# Arrange to add the fields to UserSocialAuth.extra_data
SOCIAL_AUTH_LINKEDIN_EXTRA_DATA = [('id', 'id'),
                                   ('firstName', 'first_name'),
                                   ('lastName', 'last_name'),
                                   ('emailAddress', 'email_address'), ]
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/dashboard'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/dashboard/account-settings'
LOGIN_URL = '/signin/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/dashboard/account-settings'
SOCIAL_AUTH_CLEAN_USERNAMES = True
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = False

CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'toolbar': 'full',
    },
}

MESSAGE_TAGS = {
    constants.ERROR: 'danger',
    50: 'critical',
}