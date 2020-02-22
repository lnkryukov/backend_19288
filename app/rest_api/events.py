from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from .. import events_logic


bp = Blueprint('events', __name__, url_prefix='/event')


@bp.route('/<int:id>', methods=['GET'])
def event_by_id(id):
    return jsonify(events_logic.get_event_info(id))


@bp.route('/<int:id>', methods=['PUT'])
def event_by_id(id):
    pass


@bp.route('/', methods=['POST'])
@login_required
def create_event():
    data = request.get_json()
    if not data:
        return make_415('Expected json')

    last_id = events_logic.create_event(current_user.id, data)
    # create_event_manager if exists

    return make_201(str(last_id))


@bp.route('/all', methods=['GET'])
def events():
    offset = request.args.get("offset", "")
    size = request.args.get("size", "")
    return jsonify(events_logic.get_events(offset, size))


#-------------------------- TODO --------------------------

@bp.route('/join', methods=['POST'])
@login_required
def join():
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
