from . import auth
from .config import cfg
from .rest_api import accounts, users, events
from .rest_api import *

from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from gevent import monkey

import logging


app = Flask(__name__)
app.config.update(
    DEBUG=cfg.DEBUG,
    CSRF_ENABLED=cfg.CSRF_ENABLED,
    SECRET_KEY=cfg.SECRET_KEY,
)

app.register_blueprint(accounts.bp)
app.register_blueprint(users.bp)
app.register_blueprint(events.bp)
app.register_error_handler(401, restful_api.unauthorized)
app.register_error_handler(403, restful_api.no_access)
app.register_error_handler(404, restful_api.route_not_found)
app.register_error_handler(405, restful_api.method_not_allowed)
app.register_error_handler(415, restful_api.wrong_request_type)

CORS(app)

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    level=logging.INFO)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(auth.user_loader)
login_manager.blueprint_login_views = {'restfulapi': '/login'}


def run():
    monkey.patch_all(ssl=False)
    http_server = WSGIServer((cfg.HOST, cfg.PORT), app)
    logging.info('Started server')
    http_server.serve_forever()
