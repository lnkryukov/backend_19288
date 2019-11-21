from types import SimpleNamespace
import os


cfg = SimpleNamespace()


def _get_db_connection_string():
    db_connection_string = os.getenv('DB_CONNECTION_STRING')
    if db_connection_string:
        return db_connection_string
    return 'postgresql://evpr:evrp123456789@localhost:5432/evpr'
    #return 'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'.format(**os.environ)


cfg.DEBUG = True if os.getenv('DEBUG') else False
cfg.CSRF_ENABLED = False if os.getenv('DISABLE_CSRF') else True
cfg.SECRET_KEY = os.getenv('SECRET_KEY', 'Top Secret Key, do not use in production!!!')
cfg.AUTH_HEADER_NAME = os.getenv('AUTH_HEADER_NAME', 'X-KEK-Token')
cfg.HOST = os.getenv('HOST_ADDR', '0.0.0.0')
cfg.PORT = int(os.getenv('PORT', '8080'))
cfg.DB_CONNECTION_STRING = _get_db_connection_string() 
cfg.RUNTIME_FOLDER = os.path.dirname(os.path.abspath(__file__))
cfg.SCPITS_FOLDER = os.getenv('SCRIPT_FOLDER', '{}/haslm/scripts'.format(cfg.RUNTIME_FOLDER))
