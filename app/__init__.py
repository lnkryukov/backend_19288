from . import auth
from .config import cfg
from .rest_api import accounts, users, events
from .rest_api import *
from .exceptions import *
from sqlalchemy.exc import IntegrityError

from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from gevent import monkey

import logging


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=cfg.CSRF_ENABLED,
    SECRET_KEY=cfg.SECRET_KEY,
)

app.register_blueprint(accounts.bp)
app.register_blueprint(users.bp)
app.register_blueprint(events.bp)

app.register_error_handler(401, rest_api.unauthorized)
app.register_error_handler(403, rest_api.no_access)
app.register_error_handler(404, rest_api.route_not_found)
app.register_error_handler(405, rest_api.method_not_allowed)
app.register_error_handler(415, rest_api.wrong_request_type)

app.register_error_handler(IntegrityError, rest_api.make_400)
app.register_error_handler(KeyError, rest_api.make_400)
app.register_error_handler(AttributeError, rest_api.make_400)
app.register_error_handler(WrongIdError, rest_api.make_404)
app.register_error_handler(RegisterUserError, rest_api.make_409)
app.register_error_handler(ConfirmationLinkError, rest_api.make_409)
app.register_error_handler(WrongDataError, rest_api.make_422)
app.register_error_handler(ValueError, rest_api.make_422)

CORS(app)

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    level=logging.INFO)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(auth.user_loader)


def run():
    monkey.patch_all(ssl=False)
    http_server = WSGIServer((cfg.HOST, cfg.PORT), app)
    logging.info('Started server')
    http_server.serve_forever()
