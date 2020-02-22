from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from .. import users_logic


bp = Blueprint('users', __name__, url_prefix='/user')


@bp.route('/', methods=['GET'])
@login_required
def user():
    return jsonify(users_logic.get_user_info(current_user.id))


@bp.route('/status', methods=['GET'])
@login_required
def user_status():
    return jsonify(current_user.account_status)


@bp.route('/', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()
    if not data:
        return make_415('Expected json')
    users_logic.update_profile(current_user.id, data)
    return make_200('Profile info successfully updated.')


@bp.route('/events/<role>', methods=['GET'])
@login_required
def user_events(role):
    if role in ['creator', 'manager', 'presenter', 'viewer']:
        offset = request.args.get("offset", "")
        size = request.args.get("size", "")
        return jsonify(users_logic.get_user_events_by_role(current_user.id,
                                                           role,
                                                           offset, size)
        )
    else:
        return make_422('Unknown role requested.')


# админка

@bp.route('/all', methods=['GET'])
def users_all():
    if current_user.service_status is not 'user':
        offset = request.args.get("offset", "")
        size = request.args.get("size", "")
        return jsonify(users_logic.get_users(offset, size)
        )
    else:
        return make_403("No rights!")


@bp.route('/<int:id>', methods=['GET'])
@login_required
def user_by_id(id):
    if current_user.service_status is not 'user':
        return jsonify(users_logic.get_user_info(id))
    else:
        return make_403("AccessError - No rights.")


@bp.route('/<int:id>/events/<role>', methods=['GET'])
@login_required
def user_by_id_events(id, role):
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


# test routes

@bp.route('/test', methods=['POST'])
@login_required
def test():
    data = request.get_json()
    if not data:
        return make_400('Expected json')

    users_logic.update_profile(current_user.id, data)
    return make_200('Profile info successfully updated.', current_user.name)
