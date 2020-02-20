from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from .. import users_logic

from ..exceptions import NotJsonError, NoData, WrongDataError, WrongIdError
from sqlalchemy.exc import IntegrityError


bp = Blueprint('users', __name__, url_prefix='/user')


@bp.route('/', methods=['GET'])
@login_required
def user():
    try:
        return jsonify(users_logic.get_user_info(current_user.id))
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))


@bp.route('/status', methods=['GET'])
@login_required
def user_status():
    try:
        return jsonify(current_user.account_status)
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))


@bp.route('/', methods=['PUT'])
@login_required
def update_profile():
    try:
        data = request.get_json()
        if not data:
            return make_415('Expected json', None)
        users_logic.update_profile(current_user.id, data)
        return make_200('Profile info successfully updated.')
    except AttributeError as e:
        return make_400('One ore more attribute is invalid. {}'.format(str(e)))
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))


@bp.route('/events/<role>', methods=['GET'])
@login_required
def user_events(role):
    try:
        if role in ['creator', 'manager', 'presenter', 'viewer']:
            offset = request.args.get("offset", "")
            size = request.args.get("size", "")
            return jsonify(users_logic.get_user_events_by_role(current_user.id,
                                                               role,
                                                               offset, size)
            )
        else:
            return make_422('Unknown role requested.')
    except KeyError as e:
        return make_415('KeyError - {}'.format(str(e)), e)
    except WrongDataError as e:
        return make_422('WrongDataError - {}'.format(str(e)))
    except ValueError as e:
        return make_422('ValueError - {}'.format(str(e)))
    except Exception as e:
        return make_400('Problem - {}'.format(str(e)))


# админка

@bp.route('/all', methods=['GET'])
def users_all():
    try:
        if current_user.service_status is not 'user':
            offset = request.args.get("offset", "")
            size = request.args.get("size", "")
            return jsonify(users_logic.get_users(offset, size)
            )
        else:
            return make_403("AccessError - No rights.")
    except Exception as e:
        return make_400('Problem - {}'.format(str(e)))


@bp.route('/<int:id>', methods=['GET'])
@login_required
def user_by_id(id):
    try:
        if current_user.service_status is not 'user':
            return jsonify(users_logic.get_user_info(id))
        else:
            return make_403("AccessError - No rights.")
    except WrongIdError as e:
        return make_422('WrongIdError - {}'.format(str(e)))
    except Exception as e:
        return make_400('Problem - {}'.format(str(e)))


@bp.route('/<int:id>/events/<role>', methods=['GET'])
@login_required
def user_by_id_events(id, role):
    try:
        if current_user.service_status is not 'user':
            if role in ['creator', 'manager', 'presenter', 'viewer']:
                offset = request.args.get("offset", "")
                size = request.args.get("size", "")
                return jsonify(users_logic.get_user_events_by_role(id, role,
                                                                   offset, size)
                )
            else:
                return make_422('Unknown role requested.')
        else:
            return make_403("AccessError - No rights.")
    except KeyError as e:
        return make_415('KeyError - {}'.format(str(e)), e)
    except WrongIdError as e:
        return make_422('WrongIdError - {}'.format(str(e)))
    except WrongDataError as e:
        return make_422('WrongDataError - {}'.format(str(e)))
    except ValueError as e:
        return make_422('ValueError - {}'.format(str(e)))
    except Exception as e:
        return make_400('Problem - {}'.format(str(e)))


# test routes

@bp.route('/test', methods=['POST'])
@login_required
def test():
    try:
        data = request.get_json()
        if not data:
            return make_400('Expected json')

        users_logic.update_profile(current_user.id, data)
        return make_200('Profile info successfully updated.', current_user.name)
    except AttributeError as e:
        return make_400('One ore more attribute is invalid. {}'.format(str(e)))
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))
