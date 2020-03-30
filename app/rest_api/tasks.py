from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from ..logic import tasks as tasks_logic, events as events_logic


bp = Blueprint('tasks', __name__, url_prefix='/event')


@bp.route('/<int:e_id>/task', methods=['POST'])
@login_required
def create_task(e_id):
    data = get_json()
    if events_logic.check_participation(current_user.id, e_id) is not 'creator':
        return make_4xx(403, "No rights")
    tasks_logic.create_task(e_id, data)
    return make_ok(201, 'Task was added')


@bp.route('/<int:e_id>/task/<int:t_id>/delete', methods=['GET'])
@login_required
def delete_task(e_id, t_id):
    if events_logic.check_participation(current_user.id, e_id) is not 'creator':
        return make_4xx(403, "No rights")
    tasks_logic.delete_task(e_id, t_id)
    return make_ok(200, 'Task was deleted')


@bp.route('/<int:e_id>/task/<int:t_id>/move/<status>', methods=['PUT'])
@login_required
def move_task(e_id, t_id, status):
    if events_logic.check_participation(current_user.id, e_id) is not 'manager':
        return make_4xx(403, "No rights")
    if status not in ['todo', 'inprocess', 'waiting', 'done']:
        return make_4xx(422, "Wrong status")
    tasks_logic.move_task(e_id, t_id, status)
    return make_ok(200, "Task's status was changed")


@bp.route('/<int:e_id>/task/all', methods=['GET'])
@login_required
def get_tasks(e_id):
    if events_logic.check_participation(current_user.id, e_id) not in ['creator', 'manager']:
        return make_4xx(403, "No rights")
    return jsonify(tasks_logic.get_tasks(e_id))


@bp.route('/<int:e_id>/task/<int:t_id>', methods=['PUT'])
@login_required
def update_task(e_id, t_id):
    data = get_json()
    if events_logic.check_participation(current_user.id, e_id) not in ['creator', 'manager']:
        return make_4xx(403, "No rights")
    tasks_logic.update_task(e_id, t_id, data)
    return make_ok(200, "Task was updated")
