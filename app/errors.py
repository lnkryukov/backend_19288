from .rest_api import *
from .exceptions import *
from sqlalchemy.exc import IntegrityError


def add_error_handlers(app):
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
    app.register_error_handler(NotJsonError, rest_api.make_415)
    app.register_error_handler(WrongDataError, rest_api.make_422)
    app.register_error_handler(ValueError, rest_api.make_422)


def on_json_loading_failed(err, e):
    raise NotJsonError('Wrong json!')
