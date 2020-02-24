from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user, fresh_login_required,
                         user_needs_refresh)

import bcrypt

from . import *
from .. import auth, accounts_logic


bp = Blueprint('accounts', __name__)


@bp.route('/login', methods=['POST'])
def login():
    try:
        if current_user.is_authenticated:
            return make_409('User is currently authenticated!')
        else:
            data = request.get_json()
            if not data:
                return make_415('Expected json!')
            user = auth.check_user(data['mail'])
            if user:
                pw = str(data['password']).encode('utf-8')
                upw = str(user.password).encode('utf-8')
                if bcrypt.checkpw(pw, upw):
                    login_user(user)
                    return make_200('User was logined', user.service_status)
                else:
                    return make_422('Invalid password')
            else:
                return make_422('Invalid user')


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return make_200('User was logouted')


@bp.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return make_409('User is currently authenticated!')
    else:
        data = request.get_json()
        if not data:
            return make_415('Expected json!')

        pw = bcrypt.hashpw(str(data['password']).encode('utf-8'),
                           bcrypt.gensalt())
        accounts_logic.register_user(data['mail'], data['name'],
                                     data['surname'], pw.decode('utf-8'))
        return make_201('User was registered.')


@bp.route('/confirm', methods=['POST'])
def confirm():
    data = request.get_json()
    if not data:
        return make_415('Expected json')
    accounts_logic.confirm_user(data['link'])
    return make_200('User was confirmed')


@bp.route('/change_password', methods=['POST'])
@fresh_login_required
def change_password():
    data = request.get_json()
    if not data:
        return make_415('Expected json')
    user = accounts_logic.change_password(current_user.id,
                                          data['old_password'],
                                          data['new_password'])
    if user:
        login_user(user)
        return make_200('Password has beed changed', user.service_status)
    else:
        return make_422('Invalid password')


@bp.route('/close_all_sessions', methods=['POST'])
@fresh_login_required
def close_all_sessions():
    data = request.get_json()
    if not data:
        return make_415('Expected json')
    user = accounts_logic.close_all_sessions(current_user.id,
                                             data['password'])
    if user:
        login_user(user)
        return make_200('Logout from all other sessions.', user.service_status)
    else:
        return make_422('Invalid password')


bp.route('/delete', methods=['POST'])
@fresh_login_required
def self_delete():
    data = request.get_json()
    if not data:
        return make_415('Expected json')
    ans = accounts_logic.self_delete(current_user.id, password)
    if ans:
        logout_user()
        return make_200('Successfully delete account.')
    else:
        return make_422('Invalid password')


@bp.route('/user/<int:id>/ban', methods=['GET'])
@login_required
def ban_user_by_id(id):
    if current_user.service_status is not 'user':
        accounts_logic.ban_user(id)
        return make_200('Successfully baned this user')
    else:
        return make_403("No rights!")
