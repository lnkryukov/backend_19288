from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from .. import users_logic, events_logic

from ..exceptions import NotJsonError, NoData, WrongDataError
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
def user_creator(role):
    try:
        if role in ['creator', 'manager', 'presenter', 'viewer']:
            offset = request.args.get("offset", "")
            size = request.args.get("size", "")
            return jsonify(users_logic.get_user_events_by_role(current_user.id,
                                                               role,
                                                               offset,
                                                               size)
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


# legacy routes - need to rework

@bp.route('/join', methods=['POST'])
@login_required
def join():
    try:
        data = request.get_json()
        if not data:
            return make_400('Expected json')

        if events_logic.event_exist(int(data['event_id'])):
            join = events_logic.join_event(current_user.id,
                                        int(data['event_id']), data['role'])
            if join:
                return make_400(join)
            return make_200('Guest joined event')
        else:
            return make_400('No such event')
    except Exception as e:
        return make_400('Problem.\n{}'.format(str(e)))


@bp.route('/users', methods=['GET'])
def users():
    try:
        return jsonify(users_logic.get_users())
    except Exception as e:
        return make_400('Problem.\n{}'.format(str(e)))


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
