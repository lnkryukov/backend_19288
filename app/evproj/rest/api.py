from flask import Blueprint, jsonify, request, make_response

from passlib.hash import sha256_crypt

from ..core import api

from ..core.exceptions import NotJsonError, NoData
from sqlalchemy.exc import IntegrityError


mod = Blueprint('api', __name__, url_prefix='/api')


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



@mod.route('/events', methods=['GET'])
def get_all_machines():
    try:
        return jsonify(api.get_events())
    except Exception as e:
        return make_400('Problem.\n{}'.format(str(e)))
