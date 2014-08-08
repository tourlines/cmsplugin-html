# coding: utf-8
import os
import sys
from decouple import config
from django.conf import settings
from dj_database_url import parse as db_url
from test_project import mommy_generators as Generators
from unipath import Path


BASE_DIR = Path(__file__).parent
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY', default='XXXXXXXXX')

AMBIENTE_TESTES_GERAL = True

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + BASE_DIR.child('db.sqlite3'),
        cast=db_url
    ),
}

PROJECT_APPS = (
    'test_project.core',
    'cmsplugin_html',
    'cmsplugin_javascript',
)

INSTALLED_APPS = (
    # Admin para o django CMS
    'djangocms_admin_style',

    # Bibliotecas padrões do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Bibliotecas Externas
    'south',
    'django_jenkins',

    # Aplicações para testes
    'django_nose',

    # Django CMS
    'cms',
    'mptt',
    'menus',
    'sekizai',

    'djangocms_link',
    'djangocms_text_ckeditor',
    'djangocms_googlemap',
    'djangocms_column',

    'filer',
    'easy_thumbnails',

    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_video',
    'form_designer',
    'form_designer.contrib.cms_plugins.form_designer_form',

) + PROJECT_APPS

TESTING = 'test' in sys.argv or 'jenkins' in sys.argv

MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + (
    # Django CMS
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-br'
LANGUAGES = (
    ('pt-br', u'Português'),
)

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Templates

TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
    'cms.context_processors.cms_settings',
    'sekizai.context_processors.sekizai',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = BASE_DIR.child('staticfiles')
STATIC_URL = config('STATIC_URL', default='/static/')

# Media files (user uploaded files)

MEDIA_ROOT = BASE_DIR.child('media')
MEDIA_URL = config('MEDIA_URL', default='/media/')

# NoseTests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--nologcapture',
    '--nocapture',
    '--verbosity=1',
]

# Estes argumentos exibem muitas informações na sua saída, estas informações
# são usadas pelo jenkins para relatorio e portanto apenas devem ser exibidas
# quando estiver no ambiente do jenkins.
if os.environ.get('JENKINS'):
    NOSE_ARGS += [
        '--with-xcoverage',
        '--cover-erase',
        '--with-xunit',
        '--xunit-file=%s' % (os.path.join(ROOT_PATH, 'reports/junit.xml')),
        '--xcoverage-file=%s' % (
            os.path.join(ROOT_PATH, 'reports/coverage.xml')),
    ]

# O argumento where do nose deve SEMPRE estar no final das opções. Ele diz ao
# nose em qual workspace o mesmo esta trabalhando possibilitando a inserção de
# varios workspaces e devido a esta carateristica quaisquer nomes que estejam
# após a esta opção é tratada como uma pasta onde ele vai buscar os testes
NOSE_ARGS.append('--where=%s' % (ROOT_PATH))

# Django-Jenkins
JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_flake8',
    #'django_jenkins.tasks.run_sloccount',
)
JENKINS_TEST_RUNNER = 'django_jenkins.runner.CITestSuiteRunner'


# Django CMS:

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

# Django CMS Plugins:

# Integração Filer e Text Editor
# SEE: https://github.com/stefanfoulis/cmsplugin-filer#integrations
TEXT_SAVE_IMAGE_FUNCTION = \
    'cmsplugin_filer_image.integrations.ckeditor.create_image_plugin'

# Para suportar telas de retina
# SEE: http://django-filer.readthedocs.org
# /en/latest/installation.html#configuration
THUMBNAIL_HIGH_RESOLUTION = True

# Easy Install
SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}

# Django Filer
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

MOMMY_CUSTOM_FIELDS_GEN = {
    'filer.fields.image.FilerImageField': Generators.gen_filer_image_field,
    'django.db.models.fields.CommaSeparatedIntegerField': Generators.gen_comma_separated_integer_field
}
