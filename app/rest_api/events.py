from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from .. import auth, users_logic, events_logic

from ..exceptions import NotJsonError, NoData
from sqlalchemy.exc import IntegrityError


bp = Blueprint('events', __name__)


@bp.route('/event', methods=['POST'])
@login_required
def create_event():
    try:
        data = request.get_json()
        if not data:
            return make_400('Expected json')

        last_id = events_logic.create_event(data)
        events_logic.create_event_creator(current_user.id, last_id)
        # create_event_manager if exists

        return make_201(str(last_id))
    except KeyError as e:
        return make_415('KeyError - \n{}'.format(str(e)))
    except IntegrityError as e:
        return make_400('IntegrityError - \n{}'.format(str(e)))
    except Exception as e:
        return make_400('Problem - \n{}'.format(str(e)))


@bp.route('/events', methods=['GET'])
def events():
    try:
        return jsonify(events_logic.get_events())
    except Exception as e:
        return make_400('Problem.\n{}'.format(str(e)))


@bp.route('/event/<int:id>', methods=['GET'])
def event(id):
    try:
        if events_logic.event_exist(id):
            return jsonify(events_logic.event_info(id))
        else:
            return make_400('No such event')
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))


#-------------------------- TODO --------------------------

@bp.route('/event', methods=['PUT'])
@login_required
def update_event():
    try:
        pass
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))
