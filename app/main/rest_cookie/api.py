from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from .. import auth, users_logic, events_logic

from ..exceptions import NotJsonError, NoData
from sqlalchemy.exc import IntegrityError


bp = Blueprint('api', __name__)


def make_400(text='Invalid reqeust'):
    body = jsonify(error=text)
    return make_response(body, 400)


def make_ok(description=None, params=None):
    body = {
        'status': 'ok',
    }
    if description:
        body['description'] = description
    if params:
        body['params'] = params
    return jsonify(body)


def unauthorized(e):
    return jsonify(error="Unauthorized"), 401


def route_not_found(e):
    return jsonify(error="Unknown route!"), 404


def method_not_allowed(e):
    return jsonify(error="Wrong route method!"), 405


@bp.route('/login', methods=['POST'])
def login():
    try:
        if current_user.is_authenticated:
            return make_400('User is currently authenticated')
        else:
            args = request.get_json()
            if not args:
                return make_400('Expected json')
            user = auth.check_user(args['mail'])
            if user:
                pw = str(args['password']).encode('utf-8')
                upw = str(user.password).encode('utf-8')
                if bcrypt.checkpw(pw, upw):
                    login_user(user)
                    return make_ok('User was logined')
                else:
                    return make_400('Invalid password')
            else:
                return make_400('Invalid user')
    except Exception as e:
        return make_400('Problem - \n{}'.format(str(e)))


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        logout_user()
        return make_ok('User was logouted')
    except Exception as e:
        return make_400('Problem - \n{}'.format(str(e)))


@bp.route('/register', methods=['POST'])
def register():
    try:
        if current_user.is_authenticated:
            return make_400('User is currently authenticated')
        else:
            args = request.get_json()
            if not args:
                return make_400('Expected json')

            pw = bcrypt.hashpw(str(args['password']).encode('utf-8'),
                               bcrypt.gensalt())
            users_logic.register_user(args['mail'], args['name'],
                                      args['surname'], pw.decode('utf-8'))
            return make_ok('User was registered')
    except KeyError as e:
        return make_400('KeyError - \n{}'.format(str(e)))
    except IntegrityError:
        return make_400('User with this login already exists')


@bp.route('/confirm', methods=['POST'])
def confirm():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')
        users_logic.confirm_user(args['link'])
        return make_ok('User was confirmed')
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))


@bp.route('/create_event', methods=['POST'])
@login_required
def create_event():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')

        last_id = events_logic.create_event(args['name'],
                                         args['sm_description'],
                                         args['description'],
                                         args['date_time'])
        events_logic.create_event_creator(current_user.id, last_id)

        return make_ok('Event was created', str(last_id))
    except KeyError as e:
        return make_400('KeyError - \n{}'.format(str(e)))
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


@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    try:
        as_creator, as_presenter, as_participant = events_logic.get_user_stat(current_user.id)
        return jsonify(creator=as_creator, presenter=as_presenter,
                       participant=as_participant)
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))


@bp.route('/join', methods=['POST'])
@login_required
def join():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')

        if events_logic.event_exist(int(args['event_id'])):
            join = events_logic.join_event(current_user.id,
                                        int(args['event_id']), args['role'])
            if join:
                return make_400(join)
            return make_ok('Guest joined event')
        else:
            return make_400('No such event')
    except Exception as e:
        return make_400('Problem.\n{}'.format(str(e)))


@bp.route('/update_event', methods=['POST'])
@login_required
def update_event():
    try:
        pass
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))


@bp.route('/test', methods=['POST'])
def test():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')
        
        events_logic.test(int(args['user_id']), args)
        return make_ok()
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))
