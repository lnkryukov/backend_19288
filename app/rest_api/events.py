from flask import Blueprint, jsonify, request, abort
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from .. import events_logic


bp = Blueprint('events', __name__, url_prefix='/event')


@bp.route('/<int:e_id>', methods=['GET'])
def event_by_id(e_id):
    if current_user.is_authenticated:
        return jsonify(part=events_logic.check_participation(current_user.id, e_id),
                       event=events_logic.get_event_info(e_id))
    else:
        return jsonify(part='not joined',
                       event=events_logic.get_event_info(e_id))


@bp.route('/<int:e_id>', methods=['PUT'])
@login_required
def put_event_by_id(e_id):
    if (current_user.service_status is not 'user' or
        events_logic.check_participation(current_user.id, e_id) in ['creator', 'manager']):
        data = get_json()

        events_logic.update_event(e_id, data)
        return make_200('Successfully updated.')
    else:
        return make_403("No rights!")


@bp.route('/', methods=['POST'])
@login_required
def create_event():
    data = get_json()

    last_id = events_logic.create_event(current_user.id, data)
    # create_event_manager if exists

    return make_201(str(last_id))


@bp.route('/all', methods=['GET'])
def events():
    offset = request.args.get("offset", "")
    size = request.args.get("size", "")
    return jsonify(events_logic.get_events(offset, size))


@bp.route('/<int:e_id>/join', methods=['POST'])
@login_required
def join(e_id):
    data = get_json()

    events_logic.join_event(current_user.id, e_id, data)
    return make_200('Successfully joined')


@bp.route('/<int:e_id>/presenters', methods=['GET'])
def presenters(e_id):
    data = get_json()

    return jsonify(events_logic.get_presenters(e_id))
