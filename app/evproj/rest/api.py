from flask import Blueprint, jsonify, request, make_response

from passlib.hash import sha256_crypt

from ..core import api

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


@mod.route('/register_user', methods=['POST'])
def register_user():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')

        api.register_user(args['mail'], args['name'], args['surname'],
                          sha256_crypt.encrypt(str(args['password'])))
        return make_ok('User was registered')
    except KeyError as e:
        return make_400('KeyError - \n{}'.format(str(e)))
    except IntegrityError:
        return make_400('User with this login already exists')


@mod.route('/event_create', methods=['POST'])
def event_create():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')

        user_id = api.get_id_by_mail(args['mail'])
        if user_id == -1:
            return make_400('Unknown user')

        last_id = api.create_event(args['name'], args['sm_description'],
                                   args['description'], args['date_time'],
                                   args['phone'], args['mail'])
        api.create_event_creator(user_id, last_id)
        if args['presenters'] != '':
            api.create_event_presenters(args['presenters'], last_id)

        return make_ok('Event was created', str(last_id))
    except KeyError as e:
        return make_400('KeyError - \n{}'.format(str(e)))
    except IntegrityError as e:
        return make_400('IntegrityError - \n{}'.format(str(e)))


@mod.route('/events', methods=['GET'])
def get_all_machines():
    try:
        return jsonify(api.get_events())
    except Exception as e:
        return make_400('Problem.\n{}'.format(str(e)))
