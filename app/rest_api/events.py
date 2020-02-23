from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from .. import events_logic


bp = Blueprint('events', __name__, url_prefix='/event')


@bp.route('/<int:id>', methods=['GET'])
def event_by_id(id):
    return jsonify(part=events_logic.check_participation(current_user.id, id),
                   event=events_logic.get_event_info(id))


@bp.route('/<int:id>', methods=['PUT'])
@login_required
def event_by_id(id):
    if current_user.service_status is not 'user' or
       events_logic.check_participation(current_user.id, id) in ['creator', 'manager']:
        data = request.get_json()
        if not data:
            return make_415('Expected json')
        events_logic.update_event(id, data)
    else:
        return make_403("No rights!")


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


@bp.route('/<int:id>/join', methods=['POST'])
@login_required
def join(id):
    data = request.get_json()
    if not data:
        return make_415('Expected json')

    events_logic.join_event(current_user.id, id, data)


@bp.route('/<int:id>/presenters', methods=['GET'])
@login_required
def join(id):
    data = request.get_json()
    if not data:
        return make_415('Expected json')

    events_logic.get_presenters(id)
