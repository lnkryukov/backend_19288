from .logic.accounts import user_loader
from .config import cfg
from .rest_api import accounts, users, events, tasks
from .errors import add_error_handlers, on_json_loading_failed

from flask import Flask, Request
from flask_login import LoginManager
from flask_cors import CORS
from flask_mail import Mail
from gevent.pywsgi import WSGIServer
from gevent import monkey

import logging
import sys


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=cfg.CSRF_ENABLED,
    SECRET_KEY=cfg.SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=False,
    REMEMBER_COOKIE_HTTPONLY=False,
    SESSION_COOKIE_DOMAIN='192.168.255.99',
    SESSION_COOKIE_PATH='/',
    MAIL_SERVER=cfg.MAIL_SERVER,
    MAIL_PORT = cfg.MAIL_PORT,
    MAIL_USERNAME = cfg.MAIL_USERNAME,
    MAIL_PASSWORD = cfg.MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER = cfg.MAIL_DEFAULT_SENDER
)

app.register_blueprint(accounts.bp)
app.register_blueprint(users.bp)
app.register_blueprint(events.bp)
app.register_blueprint(tasks.bp)

add_error_handlers(app)
Request.on_json_loading_failed = on_json_loading_failed

CORS(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(user_loader)

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    level=logging.INFO)


def run():
    monkey.patch_all(ssl=False)
    http_server = WSGIServer((cfg.HOST, cfg.PORT), app)
    logging.info('Started server')
    http_server.serve_forever()
