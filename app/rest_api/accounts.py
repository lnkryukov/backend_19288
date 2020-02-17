from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from .. import auth, accounts_logic

from ..exceptions import NotJsonError, NoData, ConfirmationLinkError, RegisterUserError
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
                return make_415('Expected json', None)
            user = auth.check_user(args['mail'])
            if user:
                pw = str(args['password']).encode('utf-8')
                upw = str(user.password).encode('utf-8')
                if bcrypt.checkpw(pw, upw):
                    login_user(user)
                    return make_200('User was logined', user.service_status)
                else:
                    return make_422('Invalid password')
            else:
                return make_422('Invalid user')
    except KeyError as e:
        return make_415('KeyError - wrong json keys', e)
    except Exception as e:
        return make_400('Problem - \n{}'.format(str(e)))


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        logout_user()
        return make_200('User was logouted')
    except Exception as e:
        return make_400('Problem - \n{}'.format(str(e)))


@bp.route('/register', methods=['POST'])
def register():
    try:
        if current_user.is_authenticated:
            return make_400('User is currently logined')
        else:
            args = request.get_json()
            if not args:
                return make_415('Expected json', None)

            pw = bcrypt.hashpw(str(args['password']).encode('utf-8'),
                               bcrypt.gensalt())
            accounts_logic.register_user(args['mail'], args['name'],
                                         args['surname'], pw.decode('utf-8'))
            return make_200('User was registered')
    except KeyError as e:
        return make_415('KeyError - wrong json keys', e)
    except RegisterUserError as e:
        return make_400('RegError - {}'.format(str(e)))
    except IntegrityError:
        return make_400('User with this mail already exists')
    except Exception as e:
        return make_400('Problem - \n{}'.format(str(e)))


@bp.route('/confirm', methods=['POST'])
def confirm():
    try:
        args = request.get_json()
        if not args:
            return make_415('Expected json', None)
        accounts_logic.confirm_user(args['link'])
        return make_200('User was confirmed')
    except KeyError as e:
        return make_415('KeyError - wrong json keys', e)
    except ConfirmationLinkError as e:
        return make_400(str(e))
    except Exception as e:
        return make_400('Problem - {}'.format(str(e)))
