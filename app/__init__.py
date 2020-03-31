from .logic.accounts import user_loader
from .config import cfg
from .rest_api import accounts, users, events, tasks
from .errors import add_error_handlers, on_json_loading_failed

from flask import Flask, Request
from flask_login import LoginManager
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from gevent import monkey
from os.path import join, exists
from os import makedirs


import logging
import sys

from prettyprinter import pprint

print(cfg.MAX_FILE_SIZE)

pprint(cfg)

for K, V in cfg.FILE_UPLOADS.FILE_SETS.items():
    print("Key: ")
    pprint(K)
    print("Value: ")
    pprint(V)
    path = join(cfg.FILE_UPLOADS.PARENT_FOLDER, V.FOLDER)
    if not exists(path):
        makedirs(path)
    cfg.FILE_UPLOADS.FILE_SETS[K].FOLDER = path

tmp_path = join(cfg.FILE_UPLOADS.PARENT_FOLDER, cfg.FILE_UPLOADS.TEMP_FOLDER)



if not exists(tmp_path):
    makedirs(tmp_path)
cfg.FILE_UPLOADS.TEMP_FOLDER = tmp_path

pprint(cfg)

app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=cfg.CSRF_ENABLED,
    SECRET_KEY=cfg.SECRET_KEY,
    MAX_CONTENT_LENGTH=cfg.MAX_FILE_SIZE,
    #SESSION_COOKIE_HTTPONLY=False,
    #REMEMBER_COOKIE_HTTPONLY=False,
    #SESSION_COOKIE_DOMAIN='192.168.255.99',
    #SESSION_COOKIE_PATH='/'
)

app.register_blueprint(accounts.bp)
app.register_blueprint(users.bp)
app.register_blueprint(events.bp)
app.register_blueprint(tasks.bp)

add_error_handlers(app)
Request.on_json_loading_failed = on_json_loading_failed

CORS(app)

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
