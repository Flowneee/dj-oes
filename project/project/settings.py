import os
import pprint

from project import ckeditor_settings

import project.private_settings as ps

BASE_DIR = ps.BASE_DIR
SECRET_KEY = ps.SECRET_KEY

DEBUG = True
DEBUG_OUTPUT = True
debug_print = pprint.PrettyPrinter(indent=4).pprint

ALLOWED_HOSTS = ps.ALLOWED_HOSTS
ADMINS = ps.ADMINS
DATABASES = ps.DATABASES

JQUERY_URL = '//code.jquery.com/jquery.min.js'

INSTALLED_APPS = (
    'bootstrap3',
    'django_admin_bootstrapped',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'macros',
    'django_ajax',
    'ckeditor',


    'accounts',
    'main',
    'tutor',
    'public_testing',
    'control_testing',
)

DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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

WSGI_APPLICATION = 'project.wsgi.application'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = '/'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# DEBUG SETTINGS #
if DEBUG:
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
        'django_extensions',
        'mmc'
    )

    # Debug Toolbar settings
    INTERNAL_IPS = ps.ALLOWED_HOSTS
    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': JQUERY_URL,
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': 'project.settings.show_toolbar',
    }

    DEBUG_TOOLBAR_PATCH_SETTINGS = False

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

    def show_toolbar(request):
        if not request.is_ajax():
            #and request.user and request.user.is_staff:
            return True
        return False

    # Django extension settings

    GRAPH_MODELS = {
      'all_applications': True,
      'group_models': True,
    }

CKEDITOR_CONFIGS = ckeditor_settings.CKEDITOR_CONFIGS
CKEDITOR_JQUERY_URL = JQUERY_URL

BOOTSTRAP3 = {
    'jquery_url': JQUERY_URL,
    'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/',
    'css_url': None,
    'theme_url': None,
    'javascript_url': None,
    'javascript_in_head': False,
    'include_jquery': False,
    'horizontal_label_class': 'col-md-3',
    'horizontal_field_class': 'col-md-9',
    'set_required': True,
    'set_disabled': False,
    'set_placeholder': True,
    'required_css_class': '',
    'error_css_class': 'has-error',
    'success_css_class': 'has-success',
    'formset_renderers': {
        'default': 'bootstrap3.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'bootstrap3.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },
}
