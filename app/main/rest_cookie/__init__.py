from .. import cfg
from ..core import auth
from . import api

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

app.register_blueprint(api.mod)
app.register_error_handler(401, api.unauthorized)
app.register_error_handler(404, api.route_not_found)
app.register_error_handler(405, api.method_not_allowed)

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    level=logging.INFO)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.user_loader(auth.user_loader)
login_manager.blueprint_login_views = {'restful': '/login'}

CORS(app)


def run():
    monkey.patch_all(ssl=False)
    http_server = WSGIServer((cfg.HOST, cfg.PORT), app)
    logging.info('Started server')
    http_server.serve_forever()
