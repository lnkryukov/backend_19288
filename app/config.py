from types import SimpleNamespace
import os


cfg = SimpleNamespace()


def _get_db_connection_string():
    db_connection_string = os.getenv('DB_CONNECTION_STRING')
    if db_connection_string:
        return db_connection_string
    return 'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'.format(**os.environ)


cfg.CSRF_ENABLED = False if os.getenv('DISABLE_CSRF') else True
cfg.SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
cfg.HOST = os.getenv('HOST_ADDR', '0.0.0.0')
cfg.PORT = int(os.getenv('PORT', '8080'))
cfg.DB_CONNECTION_STRING = _get_db_connection_string()
cfg.RUNTIME_FOLDER = os.path.dirname(os.path.abspath(__file__))
cfg.SCRIPTS_FOLDER = os.getenv('SCRIPT_FOLDER', '{}/scripts'.format(cfg.RUNTIME_FOLDER))

cfg.SUPER_ADMIN_MAIL = os.getenv('SUPER_ADMIN_MAIL')
cfg.DEFAULT_USER_STATUS = os.getenv('DEFAULT_USER_STATUS')
cfg.MAKE_ALL_LOGS = os.getenv('MAKE_ALL_LOGS', False)

cfg.SMTP_HOST = os.getenv('SMTP_HOST')
cfg.MAIL_LOGIN = os.getenv('MAIL_LOGIN')
cfg.MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
cfg.SITE_ADDR = os.getenv('SITE_ADDR')

log_levels = {
    'DISABLED': 9000,
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
    'NOTSET': 0
}

log_level = os.getenv('LOG_LEVEL')

if log_level:
    try:
        cfg.LOG_LEVEL = int(log_level)
    except:
        try:
            cfg.LOG_LEVEL = log_levels[log_level.upper()]
        except:
            cfg.LOG_LEVEL = 0
else:
    cfg.LOG_LEVEL = 0

disable_log = os.getenv('DISABLE_EXISTING_LOGGERS')
if disable_log:
    if disable_log.lower() == 'true':
        cfg.DISABLE_EXISTING_LOGGERS = True
    elif disable_log.lower() == 'false':
        cfg.DISABLE_EXISTING_LOGGERS = False
else:
    cfg.DISABLE_EXISTING_LOGGERS = False

cfg.LOGGING = { 
    'version': 1,
    'disable_existing_loggers': cfg.DISABLE_EXISTING_LOGGERS,
    'incremental': False,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': { 
        'default': { 
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'level': cfg.LOG_LEVEL
        },
    },
    'root': {
        'handlers': ['default'],
        'level': cfg.LOG_LEVEL
    },
    'loggers': { 
        '': {  # root logger
            'handlers': ['default'],
            'propagate': True,
            'level': cfg.LOG_LEVEL
        },
        'sqlalchemy': {
            'handlers': ['default'],
            'propagate': True,
            'level': 100 if cfg.DISABLE_EXISTING_LOGGERS else cfg.LOG_LEVEL
        },
        'flask_cors': {
            'handlers': ['default'],
            'propagate': True,
            'level': 100 if cfg.DISABLE_EXISTING_LOGGERS else cfg.LOG_LEVEL
        },
        'urllib3': {
            'handlers': ['default'],
            'propagate': True,
            'level': 100 if cfg.DISABLE_EXISTING_LOGGERS else cfg.LOG_LEVEL
        },
        'urllib3': {
            'handlers': ['default'],
            'propagate': True,
            'level': 100 if cfg.DISABLE_EXISTING_LOGGERS else cfg.LOG_LEVEL
        },
    }
}