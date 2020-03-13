from .accounts_logic import user_loader
from .config import cfg
from .rest_api import accounts, users, events
from .errors import add_error_handlers, on_json_loading_failed

from flask import Flask, Request
from flask_login import LoginManager
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from gevent import monkey

import logging
import logging.config
import sys

app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=cfg.CSRF_ENABLED,
    SECRET_KEY=cfg.SECRET_KEY,
    # SESSION_COOKIE_HTTPONLY=False,
    # REMEMBER_COOKIE_HTTPONLY=False,
    # SESSION_COOKIE_DOMAIN='192.168.255.99',
    # SESSION_COOKIE_PATH='/'
)

app.register_blueprint(accounts.bp)
app.register_blueprint(users.bp)
app.register_blueprint(events.bp)

add_error_handlers(app)
Request.on_json_loading_failed = on_json_loading_failed

CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(user_loader)

def run():
    monkey.patch_all(ssl=False)
    logger = logging.getLogger('gevent') if cfg.DISABLE_EXISTING_LOGGERS is False else None
    http_server = WSGIServer(
        (cfg.HOST, cfg.PORT),
        app,
        log = logger, # Gevent игнорирует конфигурацию логгеров, поэтому ему отедльно нужно сказать, чтобы перестал это делать
        error_log = logger
    )
    logging.info('Started server')
    http_server.serve_forever()
