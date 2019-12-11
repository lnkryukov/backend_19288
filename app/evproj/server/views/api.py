from .. import api
from .. import auth
from ..exceptions import NotJsonError, NoData

from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request, make_response
from flask_login import login_required, current_user


mod = Blueprint('api', __name__, url_prefix='/api')


def make_400(text='Invalid reqeust'):
    body = jsonify(error=text)
    return make_response(body, 400)


def make_ok(description=None):
    body = {
        'status': 'ok',
    }
    if description:
        body['description'] = description
    return jsonify(body)


# test routes for something)

@mod.route('/test_route', methods=['GET'])
@login_required
def test_route():
    try:
        return make_ok()
    except Exception as e:
        jsonify({'status': e})


@mod.route('/test_post', methods=['POST'])
@login_required
def test_post():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')
        print(args['domain'])
        print(args['address'])
        return make_ok()
    except Exception as e:
        jsonify({'status': e})


@mod.route('/test_post_2', methods=['POST'])
@login_required
def test_post_2():
    try:
        print(request.form['address'])
        return make_ok()
    except Exception as e:
        jsonify({'status': e})


@mod.route('/test_post_3', methods=['POST'])
@login_required
def test_post_3():
    try:
        args = request.get_json()
        print(len(args['test']))
        print(args['test'])
        return make_ok()
    except Exception as e:
        return make_400(e)
