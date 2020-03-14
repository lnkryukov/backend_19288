from types import SimpleNamespace
import os


cfg = SimpleNamespace()


def _get_db_connection_string():
    db_connection_string = os.getenv('DB_CONNECTION_STRING')
    if db_connection_string:
        return db_connection_string
    return 'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'.format(**os.environ)


cfg.HOST = os.getenv('HOST_ADDR', '127.0.0.1')
cfg.PORT = os.getenv('PORT', '8080')
cfg.DB_CONNECTION_STRING = _get_db_connection_string()
cfg.SUPER_ADMIN_MAIL = os.getenv('SUPER_ADMIN_MAIL')
