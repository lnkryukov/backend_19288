from .rest_api import *
from .util import send_500_email
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
from flask import abort


def add_error_handlers(app):
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, server_500_error)

    app.register_error_handler(HTTPException, http_error_handler)

    # legacy
    app.register_error_handler(IntegrityError, make_400)
    app.register_error_handler(KeyError, make_400)
    app.register_error_handler(AttributeError, make_400)
    app.register_error_handler(ValueError, make_422)
    app.register_error_handler(IndexError, make_422)


def http_error_handler(e):
    return jsonify(error=e.description), e.code


def on_json_loading_failed(err, e):
    abort(415, 'Expected json')
