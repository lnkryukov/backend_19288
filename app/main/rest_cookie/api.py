from flask import Blueprint, jsonify, request, make_response
from flask_login import login_required, current_user

from passlib.hash import sha256_crypt

from ..core import auth
from ..core import bl_users
from ..core import bl_events

from ..core.exceptions import NotJsonError, NoData
from sqlalchemy.exc import IntegrityError


mod = Blueprint('api', __name__)


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


def route_not_found(e):
    return jsonify(error="Unknown route!"), 404


def method_not_allowed(e):
    return jsonify(error="Wrong route method!"), 405


@mod.route('/login', methods=['POST'])
def login():
    try:
        if current_user.is_authenticated:
            return make_400('User is currently authenticated')
        else:
            args = request.get_json()
            if not args:
                return make_400('Expected json')
            user = bl_users.check_user(args['mail'])
            if user:
                if sha256_crypt.verify(args['password'], user.password):
                    login_user(user)
                    return make_ok('User was logined')
                else:
                    return make_400('Invalid password')
            else:
                return make_400('Invalid user')
    except Exception as e:
        return make_400('Problem - \n{}'.format(str(e)))


@mod.route('/register', methods=['POST'])
def register():
    try:
        if current_user.is_authenticated:
            return make_400('User is currently authenticated')
        else:
            args = request.get_json()
            if not args:
                return make_400('Expected json')

            blusers.register_user(args['mail'], args['name'], args['surname'],
                              sha256_crypt.encrypt(str(args['password'])))
            return make_ok('User was registered')
    except KeyError as e:
        return make_400('KeyError - \n{}'.format(str(e)))
    except IntegrityError:
        return make_400('User with this login already exists')


@mod.route('/create_event', methods=['POST'])
@login_required
def create_event():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')

        last_id = bl_events.create_event(args['name'],
                                         args['sm_description'],
                                         args['description'],
                                         args['date_time'])
        bl_events.create_event_creator(current_user.id, last_id)

        return make_ok('Event was created', str(last_id))
    except KeyError as e:
        return make_400('KeyError - \n{}'.format(str(e)))
    except IntegrityError as e:
        return make_400('IntegrityError - \n{}'.format(str(e)))
    except Exception as e:
        return make_400('Problem - \n{}'.format(str(e)))


@mod.route('/events', methods=['GET'])
def events():
    try:
        return jsonify(bl_events.get_events())
    except Exception as e:
        return make_400('Problem.\n{}'.format(str(e)))


@mod.route('/event/<int:id>', methods=['GET'])
def event(id):
    try:
        if bl_events.event_exist(id):
            return jsonify(bl_events.event_info(id))
        else:
            return make_400('No such event')
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))


@mod.route('/profile', methods=['GET'])
@login_required
def profile():
    try:
        as_creator, as_presenter, as_participant = bl_events.get_user_stat(current_user.id)
        return jsonify(creator=as_creator, presenter=as_presenter,
                       participant=as_participant)
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))


@mod.route('/join', methods=['POST'])
@login_required
def join():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')

        if bl_events.event_exist(int(args['event_id'])):
            bl_events.join_event(current_user.id, int(args['event_id']), args['role'])
            return make_ok('Guest joined event')
        else:
            return make_400('No such event')
    except Exception as e:
        return make_400('Problem.\n{}'.format(str(e)))
