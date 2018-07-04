import os
from enum import Enum
from kombu import Exchange, Queue


class Environments(Enum):
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'
    TESTING = 'testing'


class TokenType(Enum):
    AUTH = "AUTH"
    CONFIRMATION = "CONFIRMATION"
    PASSWORD_RESET = "PASSWORD_RESET"


class Config(object):
    # debug mode
    FLASK_DEBUG = int(os.getenv('FLASK_DEBUG', True))

    # environments
    ENVIRONMENTS = Environments

    # environment
    FLASK_ENV = os.getenv('FLASK_ENV', ENVIRONMENTS.DEVELOPMENT.value)

    # time zone
    TIME_ZONE = os.getenv('TIME_ZONE', 'America/Toronto')

    # app name
    APP_NAME = os.getenv('API_URL_PREFIX', 'FlaskApp')

    # API version
    API_VERSION = os.getenv('API_VERSION', "v1")

    # API url prefix
    API_URL_PREFIX = os.getenv('API_URL_PREFIX', '/api/%s' % API_VERSION)

    # Preferred Url Scheme
    PREFERRED_URL_SCHEME = os.getenv('PREFERRED_URL_SCHEME', 'http')

    # App host
    APP_HOST_IP = os.getenv('APP_HOST_IP', "0.0.0.0")
    APP_HOST_PORT = os.getenv('APP_HOST_PORT', 80)

    # server name
    # SERVER_NAME = 'flaskapp.com:5000'

    # Flask Mail settings - https://pythonhosted.org/Flask-Mail
    MAIL_DEBUG = int(os.getenv('MAIL_DEBUG', True))
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', None)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 465))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_USE_TLS = int(os.getenv('MAIL_USE_TLS', False))
    MAIL_USE_SSL = int(os.getenv('MAIL_USE_SSL', True))
    MAIL_MAX_EMAILS = int(os.getenv('MAIL_MAX_EMAILS', 10))
    MAIL_SUPPRESS_SEND = int(os.getenv('MAIL_SUPPRESS_SEND', False))
    MAIL_ASCII_ATTACHMENTS = int(os.getenv('MAIL_ASCII_ATTACHMENTS', False))

    # EMAILS
    DEV_EMAILS = os.getenv('DEV_EMAILS', 'change this<name@email.com>').split(',')
    ADMIN_EMAILS = os.getenv('ADMIN_EMAILS', 'first last <name@email.com>, another name <another@email.com>').split(',')
    SUPPORT_EMAILS = os.getenv('SUPPORT_EMAILS', 'name@email.com')
    MARKETING_EMAILS = os.getenv('MARKETING_EMAILS', 'name@email.com')
    EMAILS = {"DEV": DEV_EMAILS,
              "ADMIN": ADMIN_EMAILS,
              "SUPPORT": SUPPORT_EMAILS,
              "MARKETING": MARKETING_EMAILS, }

    # Supported languages
    LANGUAGES = os.getenv('LANGUAGES', "en es").split()

    JSON_SORT_KEYS = False

    # Security settings
    ENCRYPTION_TYPE_PRIORITIES = os.getenv('ENCRYPTION_TYPE_PRIORITIES', "bcrypt pbkdf2_sha256 des_crypt").split()

    # Migration directory path
    MIGRATION_DIR_PATH = os.getenv('MIGRATION_DIR', '/app/backend/flask_app/migrations')

    # Administration
    SECRET_KEY = os.getenv('SECRET_KEY', 'this-really-needs-to-be-changed')
    AUTH_SECRET_KEY = os.getenv('AUTH_SECRET_KEY', 'this-really-needs-to-be-changed+auth')
    CONFIRMATION_SECRET_KEY = os.getenv(
        'CONFIRMATION_SECRET_KEY',
        'this-really-needs-to-be-changed+confirmation')
    PASSWORD_RESET_SECRET_KEY = os.getenv(
        'CONFIRMATION_SECRET_KEY',
        'this-really-needs-to-be-changed+password-reset')

    SECRET_KEYS = {TokenType.AUTH: AUTH_SECRET_KEY,
                   TokenType.CONFIRMATION: CONFIRMATION_SECRET_KEY,
                   TokenType.PASSWORD_RESET: PASSWORD_RESET_SECRET_KEY}

    # Postgres
    POSTGRES_DATABASE_CONFIG = {
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'host': os.getenv('POSTGRES_HOST', 'db'),
        'port': os.getenv('POSTGRES_PORT', '5432'),
        'database': os.getenv('POSTGRES_DB', 'flask_app_crypto'),
    }

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s' % POSTGRES_DATABASE_CONFIG
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    # Redis
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    REDIS_HOST = os.getenv('REDIS_HOST', 'cache')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))

    if REDIS_PASSWORD is None or REDIS_PASSWORD == '':
        REDIS_CACHE_URL = os.getenv('REDIS_CACHE_URL', 'redis://%s:%d/%d' % (
            REDIS_HOST, REDIS_PORT, REDIS_DB))
    else:
        REDIS_CACHE_URL = os.getenv('REDIS_CACHE_URL', 'redis://:%s@%s:%d/%d' % (
            REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, REDIS_DB))

    # Redis Celery
    REDIS_CELERY_PASSWORD = os.getenv('REDIS_CELERY_PASSWORD', 'password')
    REDIS_CELERY_HOST = os.getenv('REDIS_CELERY_HOST', 'cache')
    REDIS_CELERY_PORT = int(os.getenv('REDIS_CELERY_PORT', 6379))
    REDIS_CELERY_DB = int(os.getenv('REDIS_CELERY_DB', 0))

    if REDIS_PASSWORD is None or REDIS_PASSWORD == '':
        REDIS_CELERY_URL = os.getenv('REDIS_CELERY_URL', 'redis://:@%s:%d/%d' % (
            REDIS_CELERY_HOST, REDIS_CELERY_PORT, REDIS_CELERY_DB))

    else:
        REDIS_CELERY_URL = os.getenv('REDIS_CELERY_URL', 'redis://:%s@%s:%d/%d' % (
            REDIS_CELERY_PASSWORD, REDIS_CELERY_HOST, REDIS_CELERY_PORT, REDIS_CELERY_DB))

    # Logging
    logging_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'custom': {
                'format': '%(levelname)s: %(asctime)s pid:%(process)s module:%(module)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'formatter': 'custom',
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.getenv('SERVER_LOG_DIR_PATH', '/app/logs/server.log'),
                'formatter': 'custom'
            },
            'file_rotate': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'custom',
                'filename': os.getenv('SERVER_LOG_DIR_PATH', '/app/logs/server.log'),
                'mode': 'a',
                'maxBytes': 10485760,
                'backupCount': 5,
            },
            'email': {
                'level': 'ERROR',
                'class': 'src.library.handlers.SSLSMTPHandler',
                'mailhost': (MAIL_SERVER, MAIL_PORT),
                'fromaddr': EMAILS['ADMIN'][0],
                'toaddrs': 'some.email@gmail.com',
                'subject': "%s Failure" % APP_NAME,
                'credentials': (MAIL_USERNAME, MAIL_PASSWORD),
                'formatter': 'custom',
                'secure': True
            },
            'email_buffer': {
                'level': 'ERROR',
                'class': 'pierky.buffered_smtp_handler.BufferedSMTPHandlerSSL',
                'mailhost': (MAIL_SERVER, MAIL_PORT),
                'fromaddr': EMAILS['ADMIN'][0],
                'toaddrs': [EMAILS['ADMIN'][0]],
                'subject': "%s Failure" % APP_NAME,
                'credentials': (MAIL_USERNAME, MAIL_PASSWORD),
                'formatter': 'custom',
                'capacity': int(os.getenv('BUFFER_BYTE_CAPACITY', 500))
            },
        },
        'loggers': {
            '': {
                'handlers': os.getenv('LOGGER_HANDLERS', 'console').split(' '),
                'level': os.getenv('LOGGER_LEVEL', 'DEBUG'),
                'propagate': True
            },
        }
    }


class CeleryConfig(object):
    """
    [Celery notes]
    config docs - http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_create_missing_queues
    example docs - https://pawelzny.com/python/celery/2017/08/14/celery-4-tasks-best-practices/
    example on how to start a worker process:
    $ celery -A src.task_worker.celery worker -l info -Q default,low_priority,high_priority -c 4
        NOTE:   Celery 4 has nasty, very hard to find bug in worker.
                It works only with 4 defined queues after -Q parameter. If you need more queues, just start more workers.
    or
    $ celery -A src.task_worker.celery worker -l info -Q default -c 2
    $ celery -A src.task_worker.celery worker -l info -Q low_priority -c 1
    $ celery -A src.task_worker.celery worker -l info -Q high_priority -c 4

    And with auto scaling workers

    $ celery -A src.task_worker.celery worker -l info -Q default --autoscale 4,2
    $ celery -A src.task_worker.celery worker -l info -Q low_priority --autoscale 2,1
    $ celery -A src.task_worker.celery worker -l info -Q high_priority --autoscale 8,4

    This way you can control tasks consumption speed.

    Keep concurrency number close to CPU cores amount.
    If server has 4 core CPU, then max concurrency should be 4. Of course bigger numbers will work but with less efficiency.
    """

    # Celery config
    CELERY_PID_FILE = os.getenv('CELERY_PID_FILE', '/tmp/celery.pid')
    CELERY_BEAT_SCHEDULE = os.getenv('CELERY_BEAT_SCHEDULE', '/data/celerybeat-schedule')
    CELERY_LOGGER_LEVEL= os.getenv('CELERY_LOGGER_LEVEL', 'DEBUG')

    task_ignore_result = True  # we don't care about the return value - this is a recommended practice
    task_eager_propagates = True
    task_create_missing_queues = True  # any queues specified that aren’t defined in task_queues will be automatically created
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    worker_prefetch_multiplier = 4  # default
    worker_redirect_stdouts_level = os.getenv('CELERYD_REDIRECT_STDOUTS_LEVEL', 'DEBUG')
    broker_url = os.getenv('REDIS_CELERY_URL', Config.REDIS_CELERY_URL)
    backend_url = os.getenv('REDIS_CELERY_URL', Config.REDIS_CELERY_URL)
    enable_utc = True
    timezone = os.getenv('CELERY_TIMEZONE', 'America/Toronto')
    task_queues = (
        Queue('default'),
        Queue('low_priority'),
        Queue('high_priority'))
