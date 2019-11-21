from .. import cfg
from . import auth
from .views import web as web_views, api as api_views

from flask import Flask
from flask_login import LoginManager
from gevent.pywsgi import WSGIServer
from gevent import monkey

import logging


app = Flask(__name__)
app.config.update(
    DEBUG=cfg.DEBUG,
    CSRF_ENABLED=cfg.CSRF_ENABLED,
    SECRET_KEY=cfg.SECRET_KEY,
    AUTH_HEADER_NAME=cfg.AUTH_HEADER_NAME,
    TEMPLATES_AUTO_RELOAD=True,
)


app.register_blueprint(web_views.mod)
app.register_blueprint(api_views.mod)
app.register_error_handler(404, web_views.page_not_found)

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    level=logging.INFO)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.user_loader(auth.user_loader)
login_manager.header_loader(auth.header_loader)
login_manager.blueprint_login_views = {
    'general': '/login',
    'api': '/api/unauthorized',
}


def run():
    monkey.patch_all(ssl=False)
    http_server = WSGIServer((cfg.HOST, cfg.PORT), app)
    http_server.serve_forever()
