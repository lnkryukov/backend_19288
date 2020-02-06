from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from .. import auth

from ..exceptions import NotJsonError, NoData
from sqlalchemy.exc import IntegrityError


bp = Blueprint('auth', __name__)


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


# OLD CODE

@bp.route('/unauthorized', methods=['GET'])
def unauthorized():
    body = jsonify(error='Unauthorized')
    return make_response(body, 401)


@bp.route('/issue_token', methods=['GET'])
@login_required
def issue_token():
    if current_user.admin:
        return jsonify(token=auth.issue_token(current_user))
    else:
        return make_400('You dont have administrator rights')



@bp.route('/token', methods=['GET'])
@login_required
def token():
    if current_user.admin:
        return jsonify(token=auth.get_token(current_user))
    else:
        return make_400('You dont have administrator rights')
